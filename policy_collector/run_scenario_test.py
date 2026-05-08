"""Customer Scenario Test - Nanjing University of Finance and Economics Continuing Education College

Scenario:
- Customer: Nanjing University of Finance and Economics Continuing Education College
- Products: Academic Management Platform, Non-Academic Management Platform, Self-Study Exam Management Platform
"""

import sys
import asyncio
from datetime import date
from typing import List, Tuple

# ============== Minimal RelationAgent Core Logic ==============

class RelationType:
    UPPER_LOWER = "Upper/Lower Law"
    SERIES = "Series Policy"
    INHERIT_REVISE = "Inherit/Revise"
    SAME_SOURCE = "Same Source"
    TOPIC_RELATED = "Topic Related"
    CITATION = "Citation"


class RelationCandidate:
    def __init__(self, doc_id_1, doc_id_2, relation_type, confidence, evidence):
        self.doc_id_1 = doc_id_1
        self.doc_id_2 = doc_id_2
        self.relation_type = relation_type
        self.confidence = confidence
        self.evidence = evidence


class RelationAgent:
    """Simplified Relation Agent"""

    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold

    async def discover_relations(self, new_policy: dict, existing_policies: List[dict]) -> List[RelationCandidate]:
        candidates = []
        for existing in existing_policies:
            candidate = await self._analyze_relation(new_policy, existing)
            if candidate and candidate.confidence >= self.similarity_threshold:
                candidates.append(candidate)
        candidates.sort(key=lambda x: x.confidence, reverse=True)
        return candidates

    async def _analyze_relation(self, policy1: dict, policy2: dict) -> RelationCandidate | None:
        relation_type, confidence, evidence = self._determine_relation_type(policy1, policy2)
        if relation_type is None:
            return None
        return RelationCandidate(
            doc_id_1=policy1.get("id", ""),
            doc_id_2=policy2.get("id", ""),
            relation_type=relation_type,
            confidence=confidence,
            evidence=evidence,
        )

    def _determine_relation_type(self, policy1: dict, policy2: dict) -> Tuple[RelationType | None, float, str]:
        issuing_authority_1 = policy1.get("issuing_authority", "")
        issuing_authority_2 = policy2.get("issuing_authority", "")
        title_1 = policy1.get("title", "")
        title_2 = policy2.get("title", "")
        publish_date_1 = self._parse_date(policy1.get("publish_date"))
        publish_date_2 = self._parse_date(policy2.get("publish_date"))
        title_similarity = self._calculate_title_similarity(title_1, title_2)

        # Same source authority
        if issuing_authority_1 and issuing_authority_1 == issuing_authority_2:
            if title_similarity > 0.8:
                return RelationType.SERIES, 0.85 + title_similarity * 0.1, \
                    f"Same source({issuing_authority_1}) + Title similarity{title_similarity:.2f}"
            else:
                return RelationType.SAME_SOURCE, 0.75, \
                    f"Same source({issuing_authority_1})"

        # Highly similar titles
        if title_similarity > 0.9:
            if publish_date_1 and publish_date_2:
                year_diff = abs((publish_date_2 - publish_date_1).days)
                if year_diff < 365:
                    return RelationType.INHERIT_REVISE, 0.9, \
                        f"High title similarity({title_similarity:.2f}) + Close timing({year_diff}days)"
                elif year_diff < 730:
                    return RelationType.SERIES, 0.85, \
                        f"High title similarity({title_similarity:.2f}) + Within 2 years"
            return RelationType.SERIES, 0.8 + title_similarity * 0.1, \
                f"High title similarity({title_similarity:.2f})"

        # Moderately similar titles
        if title_similarity > 0.6:
            return RelationType.TOPIC_RELATED, 0.6 + title_similarity * 0.2, \
                f"Title similarity{title_similarity:.2f}"

        # Check topic related
        topic_related = self._check_topic_related(policy1, policy2)
        if topic_related:
            return RelationType.TOPIC_RELATED, topic_related[0], topic_related[1]

        return None, 0.0, ""

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        if not title1 or not title2:
            return 0.0
        words1 = set(self._extract_keywords(title1.lower()))
        words2 = set(self._extract_keywords(title2.lower()))
        if not words1 or not words2:
            return 0.0
        jaccard = len(words1 & words2) / len(words1 | words2)
        levenshtein_sim = 1 - self._levenshtein_distance(title1.lower(), title2.lower()) / \
            max(len(title1.lower()), len(title2.lower()), 1)
        return jaccard * 0.6 + levenshtein_sim * 0.4

    def _extract_keywords(self, text: str) -> List[str]:
        import re
        words = re.findall(r'[\w]+', text)
        stopwords = {"de", "le", "he", "yu", "yu", "guanyu", "dui", "zai", "wei", "yi", "ji", "deng", "guanyu"}
        return [w for w in words if len(w) >= 2 and w not in stopwords]

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def _check_topic_related(self, policy1: dict, policy2: dict) -> Tuple[float, str] | None:
        content1 = policy1.get("content", "")[:1000]
        content2 = policy2.get("content", "")[:1000]
        keywords1 = self._extract_keywords(content1.lower())
        keywords2 = self._extract_keywords(content2.lower())
        if not keywords1 or not keywords2:
            return None
        common = set(keywords1) & set(keywords2)
        if len(common) >= 3:
            overlap_ratio = len(common) / min(len(keywords1), len(keywords2))
            if overlap_ratio > 0.15:
                return 0.6 + overlap_ratio * 0.2, \
                    f"Keyword overlap({len(common)}), ratio{overlap_ratio:.2f}"
        return None

    def _parse_date(self, date_str):
        if date_str is None:
            return None
        if isinstance(date_str, date):
            return date_str
        if isinstance(date_str, str):
            try:
                from datetime import datetime
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
            except ValueError:
                return None
        return None


# ============== Test Scenarios ==============

async def test_nanjing_university_edu_college_scenario():
    """
    Complete scenario test: Nanjing University of Finance and Economics Continuing Education College

    Scenario: Customer purchases Academic Management Platform, Non-Academic Management Platform,
              Self-Study Exam Management Platform
    """
    agent = RelationAgent()

    # Policy database related to this customer
    existing_policies = [
        # Academic management related
        {
            "id": "p1",
            "title": "Higher Education Academic Certificate Management Measures",
            "content": "To standardize higher education academic certificate management, ensure authenticity and validity...",
            "publish_date": date(2023, 3, 15),
            "issuing_authority": "Ministry of Education",
            "citation_id": "EDU-XUELI-001",
        },
        # Non-academic/Continuing education related
        {
            "id": "p2",
            "title": "Continuing Education Provisional Regulations",
            "content": "To develop continuing education, improve citizen quality, build a learning society...",
            "publish_date": date(2022, 9, 1),
            "issuing_authority": "Ministry of Education",
            "citation_id": "EDU-FEIXUELI-001",
        },
        {
            "id": "p3",
            "title": "Standards for Setting Up Continuing Education College in Regular Universities",
            "content": "To standardize the construction and management of continuing education colleges...",
            "publish_date": date(2021, 5, 15),
            "issuing_authority": "Ministry of Education",
            "citation_id": "EDU-JIXU-001",
        },
        # Self-study exam related
        {
            "id": "p4",
            "title": "Provisional Regulations on Higher Education Self-Study Examination",
            "content": "To encourage self-study, standardize self-study examination system, guarantee quality...",
            "publish_date": date(2022, 1, 1),
            "issuing_authority": "State Council",
            "citation_id": "GOV-ZIKAO-001",
        },
        {
            "id": "p5",
            "title": "Implementation Rules for Higher Education Self-Study Examination",
            "content": "According to 'Provisional Regulations on Higher Education Self-Study Examination'...",
            "publish_date": date(2022, 3, 20),
            "issuing_authority": "Ministry of Education",
            "citation_id": "EDU-ZIKAO-001",
        },
        # Unrelated policy
        {
            "id": "p6",
            "title": "New Energy Vehicle Industry Development Plan",
            "content": "To promote high-quality development of new energy vehicle industry...",
            "publish_date": date(2023, 1, 1),
            "issuing_authority": "State Council",
            "citation_id": "GOV-NEV-001",
        },
    ]

    # New policy: Notice on strengthening academic certificate management
    new_policy = {
        "id": "new",
        "title": "Notice on Further Strengthening Academic Certificate Management",
        "content": "To standardize academic certificate management, prevent diploma fraud...",
        "publish_date": date(2024, 6, 1),
        "issuing_authority": "Ministry of Education",
        "citation_id": "EDU-NEW-2024-001",
    }

    candidates = await agent.discover_relations(new_policy, existing_policies)

    print("\n" + "="*70)
    print("Customer Scenario Test: Nanjing University FE Continuing Education College")
    print("Products: Academic Mgmt Platform, Non-Academic Mgmt Platform, Self-Study Platform")
    print("="*70)
    print(f"\n[INPUT] Policy: {new_policy['title']}")
    print(f"[INFO] Policy database size: {len(existing_policies)} policies")
    print(f"\n[RESULT] Discovered {len(candidates)} relations")
    print("-"*70)

    for i, c in enumerate(candidates, 1):
        # Find corresponding policy info
        matched_policy = next(
            (p for p in existing_policies if p["id"] in [c.doc_id_1, c.doc_id_2] and p["id"] != "new"),
            None
        )
        print(f"\n{i}. Type: {c.relation_type}")
        print(f"   Confidence: {c.confidence:.2f}")
        print(f"   Evidence: {c.evidence}")
        if matched_policy:
            print(f"   Matched Policy: {matched_policy['title']}")

    print("\n" + "-"*70)

    # Statistics
    relation_types = {}
    for c in candidates:
        rt = c.relation_type
        relation_types[rt] = relation_types.get(rt, 0) + 1

    print("\n[SUMMARY]")
    print(f"  - Total relations found: {len(candidates)}")
    print(f"  - Relation type distribution:")
    for rt, count in relation_types.items():
        print(f"      * {rt}: {count}")

    # Verification
    print("\n[VERIFICATION]")
    if len(candidates) >= 3:
        print(f"  [PASS] Sufficient relations: {len(candidates)} >= 3")
    else:
        print(f"  [FAIL] Insufficient relations: {len(candidates)} < 3")

    all_above_threshold = all(c.confidence >= 0.75 for c in candidates)
    if all_above_threshold:
        print(f"  [PASS] All relations have confidence >= 0.75")
    else:
        print(f"  [FAIL] Some relations below threshold")

    has_same_source = RelationType.SAME_SOURCE in relation_types or RelationType.SERIES in relation_types
    if has_same_source:
        print(f"  [PASS] Correctly identified same-source relations")

    print("\n" + "="*70)
    print("Test Complete!")
    print("="*70)

    return len(candidates) >= 3 and all_above_threshold


async def test_title_similarity():
    """Test title similarity calculation"""
    agent = RelationAgent()

    test_cases = [
        ("Higher Education Academic Certificate Management Measures",
         "Higher Education Academic Certificate Management Measures", 0.9, "Identical"),
        ("Higher Education Academic Certificate Management Measures",
         "Academic Certificate Management Measures", 0.6, "Containment"),
        ("Higher Education Academic Certificate Management Measures",
         "Notice on Further Strengthening Academic Certificate Management", 0.6, "Similar topic"),
        ("Higher Education Self-Study Examination Provisional Regulations",
         "Higher Education Self-Study Examination Implementation Rules", 0.8, "Series policy"),
        ("New Energy Vehicle Industry Development Plan",
         "Academic Certificate Management Measures", 0.0, "Completely different"),
    ]

    print("\n" + "="*70)
    print("Title Similarity Test")
    print("="*70)

    all_pass = True
    for t1, t2, min_expected, desc in test_cases:
        sim = agent._calculate_title_similarity(t1, t2)
        status = "[PASS]" if sim > min_expected else "[FAIL]"
        print(f"{status} {desc}: '{t1}' vs '{t2}'")
        print(f"   Similarity: {sim:.2f} (expected > {min_expected})")
        if sim <= min_expected:
            all_pass = False
        print()

    return all_pass


async def main():
    """Main function"""
    print("\n" + "="*70)
    print("[TEST] Relation Agent Customer Scenario Test")
    print("="*70)

    # 1. Title similarity test
    title_ok = await test_title_similarity()

    # 2. Complete scenario test
    scenario_ok = await test_nanjing_university_edu_college_scenario()

    # Summary
    print("\n" + "="*70)
    print("[SUMMARY]")
    print("="*70)
    print(f"  Title similarity test: {'PASS' if title_ok else 'FAIL'}")
    print(f"  Customer scenario test: {'PASS' if scenario_ok else 'FAIL'}")
    print(f"  Overall: {'ALL PASS' if (title_ok and scenario_ok) else 'SOME FAILED'}")

    return title_ok and scenario_ok


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
