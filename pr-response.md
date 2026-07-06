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
* **My position**: I strongly support maintaining the `public=True` default parameter configuration for newly generated watchlists.
* **Reasoning**: CineLog is structurally positioned as a community film-tracking app where social proof and collective cinema discovery serve as primary utility drivers. By optimizing for public visibility by default, we reduce user onboarding friction for social loops—allowing friends to instantly view, share, and cross-reference peer watchlists without requiring manual, multi-step privacy configuration. This default behavior directly accelerates engagement and platform curation velocity.
* **Tradeoff acknowledged**: The clear tradeoff here is user privacy baseline expectations. Privacy-conscious users might assume their upcoming, uncurated lists are private until explicitly shared. To mitigate this risk without crippling platform discoverability, the system provides an optional `public` visibility argument on creation and route parameters, allowing explicit overrides while keeping the baseline social engine open.

## Comment 5 — Sort order
* **My position**: I agree with the maintainer’s preference to transition the default watchlist collection sort order from alphabetical (`Film.title.asc()`) to chronological descending based on creation timestamps (`WatchlistEntry.date_added.desc()`).
* **Reasoning**: A watchlist functions as a highly transient queue of immediate intent, fundamentally different from a static library collection. Sorting chronologically optimizes for a user's active, top-of-mind desires—instantly answering the question, "What did I just add to my list to watch tonight?" Alphabetical sorting scatters recent additions arbitrarily based on title lettering, creating a highly disjointed user experience as the ledger grows larger over time.
* **Engagement with reviewer's point**: The maintainer's observation that "most users want to see what they added recently" is entirely accurate regarding transient queue behavior. Furthermore, adopting a chronological sorting mechanism mirrors the structural design pattern established inside `services/collection_service.py` for `get_collection()`. This architectural consistency provides a predictable user experience across all profile feeds in the CineLog platform.

## Comment 6 — Rebase
* **What conflicted**: The upstream `main` branch introduced a database refactor changing `Film.id` columns from sequential integers to string-based UUID identifiers. This created a structural type mismatch with our `WatchlistEntry.film_id` column (initially written as an integer) and dropped our newly declared model out of `models.py` since it did not exist upstream yet.
* **How I resolved it**: I manually appended the `WatchlistEntry` entity schema back to the bottom of `models.py` using `db.String(36)` columns to link foreign keys correctly. I updated the non-existent mock tracking parameters in `tests/test_watchlist.py` to use a string-based mock UUID (`"00000000-0000-0000-0000-000000000000"`). I also incorporated our Comment 5 design selection by altering the query tracking array inside `get_watchlist()` to sort by `WatchlistEntry.date_added.desc()`.
* **How I verified no conflict remains**: I ran the test orchestration engine with `python -m pytest` and verified all tests pass across both components with no integrity or import failures.

## PR Description