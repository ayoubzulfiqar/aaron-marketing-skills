"""Small shared typed-framework primitives used by deterministic runtimes."""

C3_SCOPES = {"ace", "art", "roi"}
C3_GOALS = {"awareness", "engagement", "conversion", "brand-building"}
C3_ASSESSMENT_TIMES = {"forecast", "actual"}
C3_CONTEXT_FIELDS = {"scope", "goal", "assessment_time", "rollup_id"}


def validate_c3_context(context, errors, label="context", expected_scope=None,
                        expected_goal=None):
    if not isinstance(context, dict):
        errors.append("%s must be an object" % label)
        return
    extras = set(context) - C3_CONTEXT_FIELDS
    if extras:
        errors.append("%s has unknown fields: %s" % (
            label, ", ".join(sorted(repr(key) for key in extras)),
        ))
    scope = context.get("scope")
    goal = context.get("goal")
    assessment_time = context.get("assessment_time")
    rollup_id = context.get("rollup_id")
    if not isinstance(scope, str) or scope not in C3_SCOPES:
        errors.append("%s.scope must be ace, art, or roi" % label)
    elif expected_scope is not None and scope != expected_scope:
        errors.append("%s.scope must match the component profile" % label)
    if not isinstance(goal, str) or goal not in C3_GOALS:
        errors.append("%s.goal is invalid" % label)
    elif expected_goal is not None and goal != expected_goal:
        errors.append("%s.goal must match the component profile" % label)
    if not isinstance(assessment_time, str) or assessment_time not in C3_ASSESSMENT_TIMES:
        errors.append("%s.assessment_time must be forecast or actual" % label)
    if not isinstance(rollup_id, str) or not rollup_id.strip():
        errors.append("%s.rollup_id must be a non-empty string" % label)
