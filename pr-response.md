# PR Response Doc — CineLog Watchlist Feature

## AI Usage

## Comment 1 — Rename
* **What I did**: I renamed the core service function from `save_to_watchlist()` to `add_to_watchlist()` inside `services/watchlist_service.py` to align with the platform's standard `verb_to_noun` naming convention. 
* **How I verified**: I used a project-wide global text search (`Ctrl + Shift + F`) to locate all references to the old function name across the workspace. I identified and updated the matching import statements and route invocations inside `routes/watchlist/watchlist.py`. I then ran `python -m pytest` to verify the baseline tracking system remains fully functional.

## Comment 2 — Deduplication
* **What I did**: I introduced a custom exception class `AlreadyOnWatchlistError` and added a query constraint check inside `add_to_watchlist()` to see if a matching `user_id` and `film_id` record already exists in the database. If discovered, the application raises the error instead of appending a duplicate record.
* **How I verified**: I referenced the architectural pattern built into `services/collection_service.py` (specifically how `add_to_collection()` leverages `.query.filter_by().first()`) to ensure identical exception handling patterns. I then ran `python -m pytest` to verify the application's core data persistence logic remains sound.

## Comment 3 — Missing test
* **What I did**: I created a new test file `tests/test_watchlist.py` and implemented the `test_add_to_watchlist_nonexistent_film_raises()` test function.
* **How I verified**: I modeled this test suite directly after the structure found in `tests/test_collection.py`, replicating the isolated in-memory database app fixture and user seeding mechanics. I used an integer value (`999999`) to represent a non-existent film asset to match the branch's pre-refactor schema, wrapped the call inside a `pytest.raises(FilmNotFoundError)` assertion context block, and confirmed it passes successfully by running `python -m pytest tests/test_watchlist.py -v`.

## Comment 4 — Default visibility
* **My position:**
* **Reasoning:**
* **Tradeoff acknowledged:**

## Comment 5 — Sort order
* **My position:**
* **Reasoning:**
* **Engagement with reviewer's point:**

## Comment 6 — Rebase
* **What conflicted:**
* **How I resolved it:**
* **How I verified no conflict remains:**

## PR Description