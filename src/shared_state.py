from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, List

"""Which tree is currently active"""
class ActiveTreeType(str, Enum):
    AVL = "AVL"
    RED_BLACK = "RED_BLACK"
    
"""Which node is highlighted"""
@dataclass(slots=True)
class HighlightedNode:
    value: Optional[int] = None
    color: str = "yellow"
    reason: str = ""
    
"""One frame of rotation animation"""
@dataclass(slots=True)
class RotationStep:
    label: str
    snapshot_root: Any = None
    payload: dict = field(default_factory=dict)

"""Check to see if animation is running"""
@dataclass(slots=True)
class AnimationState:
    in_progress: bool = False #True while animation is playing
    step_index: int = 0
    steps: List[RotationStep] = field(default_factory=list)
    delay_ms: int = 1000

    # clears everything and ends animation
    def reset(self) -> None:
        self.in_progress = False
        self.step_index = 0
        self.steps.clear()

"""What numbers to display"""
@dataclass(slots=True)
class Metrics:
    avl_height: int = 0
    rb_height: int = 0
    
    # Rotation count will help with the report portion
    avl_rotations: int = 0
    rb_rotations: int = 0

"""Main object that holds everything"""
@dataclass(slots=True)
class AppState:
    tree_type: ActiveTreeType = ActiveTreeType.AVL # Which tree is active

    # Root pointers for each tree to toggle views
    avl_root: Any = None
    rb_root: Any = None

    # UI selection/highlight
    highlight: HighlightedNode = field(default_factory=HighlightedNode)

    # Rotation visualization
    animation: AnimationState = field(default_factory=AnimationState)

    # Global counters
    metrics: Metrics = field(default_factory=Metrics)

    # Revision counter -> bump this to tell UI “state changed”
    revision: int = 0
    status_text: str = ""

    # Returns the root for which tree is currently active
    def current_root(self) -> Any:
        return self.avl_root if self.tree_type == ActiveTreeType.AVL else self.rb_root

    # sets root of the active tree
    def set_current_root(self, root: Any) -> None:
        if self.tree_type == ActiveTreeType.AVL:
            self.avl_root = root
        else:
            self.rb_root = root

    # signals "state changed so UI should update"
    # sets the root of the active tree
    def touch(self, status: str = "") -> None:
        """Call whenever you want UI to redraw."""
        self.revision += 1
        if status:
            self.status_text = status


"""
global shared instance
- The object everyone will import
- Do not create another AppState() anywhere else, or it will break things
"""
state = AppState()

def current_display_root():
    if state.animation.in_progress and state.animation.steps:
        i = state.animation.step_index
        if 0 <= i < len(state.animation.steps):
            snap = state.animation.steps[i].snapshot_root
            if snap is not None:
                return snap
    return state.current_root()


# Helper functions to modify state and trigger redraws
# These are optional for now and might be removed later, but they can help keep things organized and ensure we always call touch().

def set_tree_type(tree_type: ActiveTreeType) -> None:
    state.tree_type = tree_type
    state.highlight = HighlightedNode()     # clear highlight on toggle (optional)
    state.animation.reset()           # stop animation on toggle (optional)
    state.touch(f"Switched to {tree_type.value}")


def begin_animation(steps: List[RotationStep], *, delay_ms: Optional[int] = None) -> None:
    state.animation.in_progress = True
    state.animation.steps = list(steps) # make a copy to be safe
    state.animation.step_index = 0
    if delay_ms is not None:
        state.animation.delay_ms = delay_ms
    state.touch("Animation started")


def advance_animation_step() -> None:
    """UI timer can call this; when done, it ends animation."""
    if not state.animation.in_progress:
        return
    state.animation.step_index += 1
    if state.animation.step_index >= len(state.animation.steps):
        state.animation.reset()
        state.touch("Animation finished")
    else:
        state.touch("Animation step")


def set_highlight(value: Optional[int], reason: str = "", color: str = "yellow") -> None:
    state.highlight.value = value
    state.highlight.reason = reason
    state.highlight.color = color
    state.touch()