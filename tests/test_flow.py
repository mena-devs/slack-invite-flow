import pytest

from slack_invite_flow import flow


def test_activity_must_abide_by_interface():
    """Tests whether a child activity can omit the required functions"""
    class FooActivity(flow.Activity):
        pass

    with pytest.raises(TypeError):
        FooActivity()


def test_single_activity_flow():
    """Tests that a single activity runs successfully within a flow"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            pass

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=0)),
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'flow complete',
    ] == actions


def test_single_activity_fail_with_no_repeat_flow():
    """Tests that a single failed activity will not be repeated on failure"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            raise Exception('fail!')

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=0)),
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'error foo',
        'flow complete',
    ] == actions


def test_single_activity_fail_with_repeat_flow():
    """Tests that a single activity will be repeated on failure"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            raise Exception('fail!')

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=2)),
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'error foo',
        'playing foo with repeat',
        'error foo',
        'playing foo with repeat',
        'error foo',
        'flow complete',
    ] == actions


def test_multiple_activities_flow():
    """Tests that multiple activities can complete successfully"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            pass

    class BarActivity(flow.Activity):
        def execute(self, **payload):
            pass

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=0)),
        ('bar', flow.ActivityConfig(kind=BarActivity, extend=True, repeat=0))
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'playing bar',
        'flow complete',
    ] == actions


def test_multiple_activities_skip_flow():
    """Tests that skipping activities is possible"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            pass

    class BarActivity(flow.Activity):
        def execute(self, **payload):
            pass

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=0)),
        ('bar', flow.ActivityConfig(kind=BarActivity, extend=True, repeat=0))
    ])

    actions = [action for _, action, _ in workflow.play(initial='bar')]

    assert [
        'starting',
        'skipping foo',
        'playing bar',
        'flow complete',
    ] == actions


def test_multiple_activities_no_fallthrough_flow():
    """Tests that activities will not fallthrough on failure if not explicitly
    set within the configuration"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            raise Exception('fail!')

    class BarActivity(flow.Activity):
        def execute(self, **payload):
            pass

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=False, repeat=0)),
        ('bar', flow.ActivityConfig(kind=BarActivity, extend=True, repeat=0))
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'error foo',
        'flow complete',
    ] == actions


def test_multiple_activities_with_fallthrough_flow():
    """Tests that activities can fallthrough on failure if explicitly set"""
    class FooActivity(flow.Activity):
        def execute(self, **payload):
            raise Exception('fail!')

    class BarActivity(flow.Activity):
        def execute(self, **payload):
            pass

    workflow = flow.ActivityFlow([
        ('foo', flow.ActivityConfig(kind=FooActivity, extend=True, repeat=0)),
        ('bar', flow.ActivityConfig(kind=BarActivity, extend=True, repeat=0))
    ])

    actions = [action for _, action, _ in workflow.play()]

    assert [
        'starting',
        'playing foo',
        'error foo',
        'playing bar',
        'flow complete',
    ] == actions
