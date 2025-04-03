import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_multiple_choices():
    question = Question(title='q1')
    
    question.add_choice('a', False)
    question.add_choice('b', True)

    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert question.choices[1].text == 'b'
    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct

def test_add_multiple_choices():
    q = Question("q")
    c1 = q.add_choice("Option A")
    c2 = q.add_choice("Option B", is_correct=True)
    assert len(q.choices) == 2
    assert c1.text == "Option A"
    assert c2.is_correct == True

def test_remove_choice_by_id():
    q = Question("q")
    c1 = q.add_choice("Para remoção")
    q.remove_choice_by_id(c1.id)
    assert len(q.choices) == 0

def test_remove_all_choices():
    q = Question("q")
    q.add_choice("Um")
    q.add_choice("Dois")
    q.remove_all_choices()
    assert q.choices == []

def test_select_correct_choices_only():
    q = Question("q", max_selections=2)
    c1 = q.add_choice("Correta", is_correct=True)
    c2 = q.add_choice("Incorreta", is_correct=False)
    selected = q.select_choices([c1.id, c2.id])
    assert selected == [c1.id]

def test_exceed_max_selections():
    q = Question("q", max_selections=1)
    c1 = q.add_choice("A")
    c2 = q.add_choice("B")
    with pytest.raises(Exception):
        q.select_choices([c1.id, c2.id])

def test_set_correct_choices():
    q = Question("q")
    c1 = q.add_choice("A")
    c2 = q.add_choice("B")
    q.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct

def test_generate_choice_id_increments():
    q = Question("q")
    c1 = q.add_choice("A")
    c2 = q.add_choice("B")
    assert c2.id == c1.id + 1

def test_choice_by_id_returns_choice():
    q = Question("q")
    c = q.add_choice("Nova escolha")
    found = q._choice_by_id(c.id)
    assert found.text == "Nova escolha"

def test_invalid_choice_id_raises():
    q = Question("q")
    q.add_choice("A")
    invalid_id = 999
    assert invalid_id not in [c.id for c in q.choices]
    with pytest.raises(Exception, match="Invalid choice id"):
        q._choice_by_id(invalid_id)

@pytest.fixture
def question_with_four_choices():
    q = Question("Question with four choices")
    q.add_choice("Option A")
    q.add_choice("Option B", is_correct=True)
    q.add_choice("Option C")
    q.add_choice("Option D", is_correct=True)
    return q

def test_correct_choice_ids(question_with_four_choices):
    q = question_with_four_choices
    correct_ids = q._correct_choice_ids()
    assert len(correct_ids) == 2
    for cid in correct_ids:
        assert q._choice_by_id(cid).is_correct

def test_sequential_choice_ids(question_with_four_choices):
    q = question_with_four_choices
    choice_ids = [choice.id for choice in q.choices]
    assert choice_ids == [1, 2, 3, 4]