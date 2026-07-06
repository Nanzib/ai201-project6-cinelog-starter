"""
tests/test_watchlist.py — CineLog

Tests for the watchlist service.
"""

import pytest
from app import create_app, db
from models import User, Film, WatchlistEntry
from services.watchlist_service import (
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist,
    FilmNotFoundError,
    AlreadyOnWatchlistError,
    NotInWatchlistError
)


@pytest.fixture
def app():
    """Create an isolated test app with an in-memory database."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """A user to use in tests."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_film(app):
    """A film to use in tests."""
    with app.app_context():
        film = Film(title="Paddington 2", year=2017, genre="Comedy")
        db.session.add(film)
        db.session.commit()
        return film.id


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(user_id=sample_user, film_id=fake_film_id)


# ── Stretch Feature 1: Removal Tests ─────────────────────────────────────────

def test_remove_from_watchlist_removes_entry(app, sample_user, sample_film):
    """Ensures a film can be successfully removed from a user's watchlist."""
    with app.app_context():
        add_to_watchlist(user_id=sample_user, film_id=sample_film)
        
        result = remove_from_watchlist(user_id=sample_user, film_id=sample_film)
        assert result is True
        
        in_db = WatchlistEntry.query.filter_by(user_id=sample_user, film_id=sample_film).first()
        assert in_db is None


def test_remove_from_watchlist_not_on_list_raises(app, sample_user, sample_film):
    """Ensures removing a film that isn't on the watchlist raises NotInWatchlistError."""
    with app.app_context():
        with pytest.raises(NotInWatchlistError):
            remove_from_watchlist(user_id=sample_user, film_id=sample_film)


# ── Stretch Feature 2 & 3: Custom Edge Case Test ─────────────────────────────

def test_add_to_watchlist_explicit_private_visibility(app, sample_user, sample_film):
    """
    Second Test Edge Case: Ensures specifying an explicit public=False parameter
    correctly overrides default settings and saves the record with private visibility.
    """
    with app.app_context():
        entry = add_to_watchlist(user_id=sample_user, film_id=sample_film, public=False)
        assert entry.public is False
        
        watchlist = get_watchlist(sample_user)
        assert watchlist[0]["public"] is False