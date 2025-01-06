from __future__ import annotations

from typing import Any, cast
from unittest.mock import MagicMock

from .grammar_graph_types import RuleChar
from .graph import Graph
from .graph_node import GraphNode
from .graph_pointer import GraphPointer

# if TYPE_CHECKING:
#     from .grammar_graph_types import Pointers
from .parse_state import ParseState


class MockGraph:
    def __init__(self):
        self.add = MagicMock(side_effect=lambda _input, pointers: pointers)

    @property
    def grammar(self):
        return "sample-grammar"


def make_mock_graph():
    return cast(Graph, MockGraph())


mock_pointers = cast(
    Any,
    # Pointers,
    {
        GraphPointer(
            GraphNode(
                RuleChar(value=[65]),
                meta={"stackId": 1, "pathId": 1, "stepId": 1},
            ),
        ),
    },
)


def describe_parse_state():
    def test_constructs_with_given_graph_and_pointers():
        parse_state = ParseState(make_mock_graph(), mock_pointers)
        assert isinstance(parse_state, ParseState)

    def test_returns_unique_rules_from_pointers():
        parse_state = ParseState(make_mock_graph(), mock_pointers)
        rules = list(parse_state.rules())
        assert len(rules) == 1
        assert isinstance(rules[0], RuleChar)
        assert rules[0].value == [65]

    def test_iterates_over_unique_rules_using_symbol_iterator():
        parse_state = ParseState(make_mock_graph(), mock_pointers)
        rules = list(parse_state.rules())
        assert len(rules) == 1
        assert isinstance(rules[0], RuleChar)

    def test_adds_new_input_and_returns_new_parse_state_with_updated_pointers():
        mock_graph = make_mock_graph()
        new_pointers = set({"rule": {"type": "char", "value": [66]}})
        mock_graph.add.mock_return_value(new_pointers)

        parse_state = ParseState(mock_graph, mock_pointers)
        new_state = parse_state.add("B")
        assert isinstance(new_state, ParseState)
        mock_graph.add.assert_called_with("B", mock_pointers)

    def test_calculates_the_size_of_unique_rules_correctly():
        mock_graph = make_mock_graph()
        parse_state = ParseState(mock_graph, mock_pointers)
        size = parse_state.size
        assert size == 1

    def test_provides_access_to_the_underlying_graph_grammar():
        mock_graph = make_mock_graph()
        parse_state = ParseState(mock_graph, mock_pointers)
        assert parse_state.grammar == "sample-grammar"

    def test_is_callable_as_a_function():
        mock_graph = make_mock_graph()
        parse_state = ParseState(mock_graph, mock_pointers)
        new_state = parse_state("B")
        assert isinstance(new_state, ParseState)

    def test_it_implements_adder_dunder_method():
        mock_graph = make_mock_graph()
        parse_state = ParseState(mock_graph, mock_pointers)
        new_state = parse_state + "B"
        assert isinstance(new_state, ParseState)
