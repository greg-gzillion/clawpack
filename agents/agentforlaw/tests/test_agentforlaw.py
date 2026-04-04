#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
from agentforlaw import LawRetriever, ConstitutionAccess, ClauseLibrary, LegalDefinitions

class TestLawRetriever:
    def test_statute_format(self):
        result = LawRetriever.get_statute("15 USC 78a")
        assert "citation" in result
        assert "url" in result
        assert "cornell.edu" in result["url"]
    
    def test_statute_invalid(self):
        result = LawRetriever.get_statute("invalid")
        assert "error" in result
    
    def test_case_search(self):
        result = LawRetriever.get_case("Marbury v Madison")
        assert "case" in result
        assert "courtlistener" in result["url"]
    
    def test_cfr_format(self):
        result = LawRetriever.get_cfr("17 CFR 240.10b-5")
        assert "citation" in result
        assert "ecfr.gov" in result["url"]

class TestConstitutionAccess:
    def test_article(self):
        result = ConstitutionAccess.get_article(1)
        assert result["article"] == 1
        assert "cornell.edu" in result["url"]
    
    def test_amendment(self):
        result = ConstitutionAccess.get_amendment(1)
        assert result["amendment"] == 1
        assert "summary" in result

class TestClauseLibrary:
    def test_list_clauses(self):
        clauses = ClauseLibrary.list_clauses()
        assert len(clauses) > 0
        assert "indemnification" in clauses
    
    def test_get_clause(self):
        result = ClauseLibrary.get_clause("indemnification")
        assert "indemnify" in result.lower()

class TestLegalDefinitions:
    def test_list_terms(self):
        terms = LegalDefinitions.list_terms()
        assert len(terms) > 0
        assert "consideration" in terms
    
    def test_define(self):
        result = LegalDefinitions.define("consideration")
        assert "value" in result["definition"].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
