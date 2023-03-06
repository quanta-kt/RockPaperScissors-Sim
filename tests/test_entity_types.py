import app


def test_beats():
    assert app.EntityType.rock.beats(app.EntityType.scissors) == app.EntityType.rock
    assert app.EntityType.paper.beats(app.EntityType.rock) == app.EntityType.paper
    assert (
        app.EntityType.scissors.beats(app.EntityType.paper) == app.EntityType.scissors
    )

    assert app.EntityType.scissors.beats(app.EntityType.rock) == app.EntityType.rock
    assert app.EntityType.rock.beats(app.EntityType.paper) == app.EntityType.paper
    assert (
        app.EntityType.paper.beats(app.EntityType.scissors) == app.EntityType.scissors
    )
