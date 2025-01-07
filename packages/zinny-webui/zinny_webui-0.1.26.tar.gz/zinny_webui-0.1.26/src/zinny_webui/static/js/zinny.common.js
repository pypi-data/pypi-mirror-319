
// Common and cross-component functions

const state = {
    title_id: null,
    survey_id: null,
    screen_type: null,
    ratings: {}, // Keyed by criterion name, e.g., { "acting_skill": "8" }
    ratings_changed: false,
    score: "--",
};

function resetRatingsState(ratings) {
    state.ratings = ratings;
    state.ratings_changed = false;
}

async function fetchAndApplyRatings() {
    const titleId = state.title_id || null;
    const surveyId = state.survey_id || null;

    if (!titleId || !surveyId) {
        ratings = {}; // Default to empty ratings
        resetRatingsState(ratings);
        return;
    }

    try {
        const ratingsResponse = await fetch(`/api/v1/ratings?title_id=${titleId}&survey_id=${surveyId}`);
        if (ratingsResponse.ok) {
            const existingRatings = await ratingsResponse.json();
            if (existingRatings == {}) {
                state.ratings = {}; // Default to empty ratings
                console.warn("zinny: No ratings found for this survey-title combination.");
            } else {
                if (existingRatings.screen_type_id) {
                    ScreenSelect.selectScreenTypeFromId(existingRatings.screen_type_id);
                }
                ratings = existingRatings.ratings || {};
                resetRatingsState(ratings);
            }
        } else {
            throw new Error(`Failed to fetch ratings: ${ratingsResponse.status}`);
        }
    } catch (error) {
        console.error("zinny: Error fetching ratings:", error);
        ratings = {}; // Default to empty ratings on error
        resetRatingsState(ratings);
    }
    state.ratings_changed = false; // false for intial load
}


document.addEventListener("resetCriteria", () => {
    console.warn("zinny: WARNING: Criteria values reset not implemented yet");
});



document.addEventListener("DOMContentLoaded", () => {
    // Initialize Survey and Title Select
    SurveySelect.fetchAllSurveys();
    TitleSelect.searchTitles;
    TitleSelect.resetTitleSearch();
    SurveySelect.setupCriteriaInteraction();
    SurveySelect.setCriteriaEditable(false);
    ScreenSelect.setupScreenTypeSelector();

    
    // Initialize Survey Filters
    const filterOptions = document.getElementById("survey-filter-options");
    const filtersContainer = document.getElementById("survey-filters-container");

    // Add event listeners for expand and collapse
    filterOptions.addEventListener("show.bs.collapse", () => {
        // filtersContainer.style.display = "block"; // Show the parent container
        filtersContainer.classList.remove("d-none"); // Remove the d-none class
    });

    filterOptions.addEventListener("hidden.bs.collapse", () => {
        // filtersContainer.style.display = "none"; // Hide the parent container
        filtersContainer.classList.add("d-none"); // Remove the d-none class
    });

    // Initialize Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach((tooltipTriggerEl) => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

});
