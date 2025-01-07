let surveyFilters = {
    preset: null,
};

const SurveySelect = (function() {


    function createSurveyCard(survey) {
        const card = document.createElement("div");
        card.className = "card mb-2";
        card.onclick = () => selectSurvey(survey.id);

        const cardBody = document.createElement("div");
        cardBody.className = "card-body";

        const cardTitle = document.createElement("h5");
        cardTitle.className = "card-title";
        cardTitle.textContent = survey.name;

        const cardDescription = document.createElement("p");
        cardDescription.className = "card-text text-muted";
        cardDescription.textContent = survey.description;

        cardBody.appendChild(cardTitle);
        cardBody.appendChild(cardDescription);
        card.appendChild(cardBody);

        return card;
    }

    async function fetchAllSurveys() {
        const surveysList = document.getElementById("surveys-list");

        try {
            const response = await fetch("/api/v1/surveys/");
            if (!response.ok) {
                throw new Error("Failed to fetch surveys");
            }

            const surveys = await response.json();
            surveysList.innerHTML = ""; // Clear previous results

            surveys.forEach((survey) => {
                surveysList.appendChild(createSurveyCard(survey));
            });            
        } catch (error) {
            console.error("zinny: Error fetching surveys:", error);
            surveysList.innerHTML = `
                <li class="list-group-item text-danger">Failed to load surveys. Please try again.</li>
            `;
        }
    }

    async function surveySearch() {
        const query = document.getElementById("survey-search-input").value.toLowerCase();
        const surveysList = document.getElementById("surveys-list");

        if (!query) {
            await fetchAllSurveys();
            return;
        }

        try {
            let apiUrl = `/api/v1/surveys/search?query=${encodeURIComponent(query)}`;
            if (surveyFilters.preset) {
                apiUrl += `&preset=${encodeURIComponent(surveyFilters.preset)}`;
            }

            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error("Failed to fetch surveys");
            }

            const results = (await response.json()).results || [];
            surveysList.innerHTML = ""; // Clear previous results

            if (results.length === 0) {
                surveysList.innerHTML = `
                    <li class="list-group-item">No surveys found.</li>
                `;
            } else {
                results.forEach((survey) => {
                    surveysList.appendChild(createSurveyCard(survey));
                });
            }
        } catch (error) {
            console.error("zinny: Error fetching surveys:", error);
            surveysList.innerHTML = `
                <li class="list-group-item text-danger">Failed to load surveys. Please try again.</li>
            `;
        }
    }

    async function selectSurvey(survey_id) {
        try {
            const surveyResponse = await fetch(`/api/v1/surveys/${survey_id}`);
            if (!surveyResponse.ok) {
                throw new Error("Failed to fetch survey details");
            }
            const surveyDetails = await surveyResponse.json();
            const surveyDefaults = surveyDetails.defaults || {};
            const surveyDefaultMarkers = surveyDefaults.markers || {};

            // Apply defaults or override markers with survey or criterion values
            systemDefaultMarkers = {
                "1": "Substandard",
                "5": "Typical",
                "10": "Exceptional",
            }

            const criteria = surveyDetails.criteria.map((criterion) => {
                // Apply defaults if markers are not explicitly set for the criterion
                criterion.markers = criterion.markers || surveyDefaultMarkers || systemDefaultMarkers;
                return criterion;
            });
            const survey_name = surveyDetails.name;

            // Update state
            state.survey_id = survey_id;
            // update state ratings and screen_type with existing values
            await fetchAndApplyRatings();

            // Update the screen type selector from state
            await ScreenSelect.prefillScreenType();

            // Replace search bar with selected survey display
            const searchBar = document.getElementById("survey-input-group");
            searchBar.innerHTML = `
                <button class="btn btn-secondary was-btn-outline" onclick="SurveySelect.handleEditButtonClick()">
                    <i class="bi bi-pencil"></i>
                </button>
                <div class="form-control bg-light">${survey_name}</div>
            `;
            searchBar.classList.add("survey-selected");
            // Clear search results and display criteria
            const surveysList = document.getElementById("surveys-list");
            surveysList.classList.add("d-none");
            surveysList.innerHTML = "";
    
            // Clear and populate UI
            const criteriaList = document.getElementById("criteria-list");
            criteriaList.innerHTML = "";
            criteria.forEach((criterion) => {
                const card = createCriterionCard(criterion);
                criteriaList.appendChild(card);
            });
            criteriaList.classList.remove("d-none");

            state.ratings_changed = false; // No changes after loading

            state.score = calculateScore(state.ratings);

            if (state.title_id) {
                enableSaveButtonState(false, "loaded");
                TitleSelect.updateScore(state.score);
            } else {
                enableSaveButtonState(false, "no_title");
            }

        } catch (error) {
            console.error("zinny: Error selecting survey:", error);
        }
    }
    
    function showCriterionInfo(criterion, event = null) {
        const modal = document.getElementById("criterion-info-modal");
        const modalDialog = modal.querySelector(".modal-dialog");
    
        const modalTitle = document.getElementById("criterion-info-modal-label");
        const modalContent = document.getElementById("criterion-info-modal-content");
    
        // Ensure the content is cleared and updated dynamically
        modalTitle.textContent = criterion.name || "No Title Available";
        modalContent.textContent = criterion.description || "No Description Available";
    
        // Dynamically position the modal
        if (event) {
            const { clientX, clientY } = event; // Get the click position
            modalDialog.style.position = "fixed";
            modalDialog.style.left = `${-modalDialog.offsetWidth / 2}px`;
            modalDialog.style.top = `${clientY - modalDialog.offsetHeight / 2}px`;
        } else {
            modalDialog.style.position = "fixed";
            modalDialog.style.left = "50%";
            modalDialog.style.top = "50%";
            modalDialog.style.transform = "translate(-50%, -50%)";
        }
    
        // Reinitialize and show the modal
        const bootstrapModal = new bootstrap.Modal(modal, {
            backdrop: true, // Ensure proper backdrop handling
            focus: true,    // Ensure focus is set to the modal
        });
        bootstrapModal.show();
    }
    
    function resetSurveySearch() {
        const searchBar = document.getElementById("survey-input-group");
        const surveysList = document.getElementById("surveys-list");
        const criteriaList = document.getElementById("criteria-list");

        // Restore original search bar
        searchBar.innerHTML = `
            <span class="input-group-text" id="survey-section">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"></path>
                </svg>
            </span>
            <input id="survey-search-input" type="text" class="form-control" placeholder="Search surveys" aria-label="Search Surveys" oninput="SurveySelect.handleSearchInput()">
            <button id="survey-filter-button" class="btn btn-secondary was-btn-outline bi bi-funnel" type="button" data-bs-toggle="collapse" data-bs-target="#survey-filter-options" aria-expanded="false" aria-controls="survey-filter-options"></button>
        `;
        surveysList.innerHTML = "";
        surveysList.classList.remove("d-none");

        criteriaList.innerHTML = "";
        criteriaList.classList.add("d-none");

        // Fetch all surveys to reset the results
        fetchAllSurveys();
    }

    // Enable or Disable Criteria Section
    document.querySelectorAll('input[name="screen_type"]').forEach((radio) => {
        radio.addEventListener('change', () => {
            const criteriaList = document.getElementById("criteria-list");
            criteriaList.querySelectorAll("input, button").forEach((element) => {
                element.disabled = !radio.checked;
            });
        });
    });
    // Function to update slider thumb style
    function updateThumbStyle(valueDisplay, rangeInput) {
        if (valueDisplay.value) {
            HeaderBar.enableSaveButton();
            rangeInput.classList.add("filled");
            rangeInput.classList.remove("cleared");
        } else {
            rangeInput.classList.add("cleared");
            rangeInput.classList.remove("filled");
        }
    }

    
    let criterionIdCounter = 0;

    function createUniqueId(base, id) {
        return `${base}-${id}`;
    }

    function clearSurveyResponses() {
        // Get the survey container or the root where criterion cards are present
        const criteriaList = document.getElementById("criteria-list");
        const valueDisplays = criteriaList.querySelectorAll('.criterion-value-display');
        const rangeInputs = criteriaList.querySelectorAll('.criterion-range');

        HeaderBar.enableSaveButton();

    
        // Clear the value displays and range inputs
        valueDisplays.forEach((valueDisplay) => {
            valueDisplay.value = "";
        });
    
        rangeInputs.forEach((rangeInput) => {
            rangeInput.value = "";
            rangeInput.classList.remove("filled");
            rangeInput.classList.add("cleared");
        });
    
    }

    function hideCriteriaList() {
        const criteriaList = document.getElementById("criteria-list");
        criteriaList.classList.add("d-none");
    }


    function showCriteriaList() {
        const criteriaList = document.getElementById("criteria-list");
        criteriaList.classList.remove("d-none");
    }

    function setCriteriaEditable(isEditable) {
        const criteriaList = document.getElementById("criteria-list");
    
        if (isEditable) {
            criteriaList.classList.remove("disabled");
        } else {
            criteriaList.classList.add("disabled");
        }
    }
    
    function setupCriteriaInteraction() {
        const criteriaList = document.getElementById("criteria-list");
        criteriaList.addEventListener("click", (event) => {
            if (criteriaList.classList.contains("disabled")) {
                event.preventDefault(); // Prevent the default interaction
                showModal("Please select a title to survey.");
            }
        });
    }
    
    function showModal(message) {
        // Create a simple modal dynamically or use an existing Bootstrap modal
        const modalContent = document.getElementById("modal-content");
        const modal = new bootstrap.Modal(document.getElementById("instruction-modal"));
    
        modalContent.textContent = message;
        modal.show();
    }
    

    function clampValue(value, min=1, max=10) {
        // Validate input
        if (!isNaN(value)) {
            if (value < min) {
                value = min;
            } else if (value > max) {
                value = max;
            }
        }
        return value;
    }

    function addUniqueID(DOMObject, genericId, id) {
        const uniqueID = createUniqueId(genericId, id);
        const element = DOMObject.querySelector(`#${genericId}`);
        element.id = uniqueID;
        element.classList.add(genericId);
        return element;
    }

    function createCriterionCard(criterion) {
        const template = document.getElementById("criterion-card-template");
        const card = template.content.cloneNode(true);
    
        // Set criterion name as a data attribute
        const cardElement = card.querySelector(".criterion-card");
        cardElement.setAttribute("data-criterion-id", criterion.id);
        cardElement.setAttribute("data-criterion-name", criterion.name);
        
        // Generate unique IDs
        const rangeInput = addUniqueID(card, "criterion-range", criterion.id);
        const valueDisplay = addUniqueID(card, "criterion-value-display", criterion.id);
        const clearButton = addUniqueID(card, "criterion-value-clear", criterion.id);

        // Populate markers dynamically
        const markers = criterion.markers || {};
        const rangeLabels = card.querySelector(".range-labels");
        rangeLabels.innerHTML = ""; // Clear existing labels
        const minMarker = markers["1"] || "";
        const midMarker = markers["5"] || "";
        const maxMarker = markers["10"] || "";

        rangeLabels.innerHTML = `
            <span>${minMarker}</span>
            <span>${midMarker}</span>
            <span>${maxMarker}</span>
        `;

        // Populate initial values from state and attach event handlers
        const existingValue = state.ratings[criterion.id] || "";
        rangeInput.value = existingValue;
        valueDisplay.value = existingValue;
        state.ratings[criterion.id] = existingValue;

        if (existingValue) {
            rangeInput.classList.add("filled");
        }
    
        // select text to be ready for new input
        valueDisplay.addEventListener("focus", () => {
            valueDisplay.select();
        });
    
        clearButton.addEventListener("click", () => {
            rangeInput.value = ""; // Reset slider
            valueDisplay.value = ""; // Clear display
            // reset thumb style to indicate no value
            updateThumbStyle(valueDisplay, rangeInput);
        });
    
        // Update other card content
        const title = card.querySelector(".text-truncate");
        title.textContent = criterion.name;
    
        const infoButton = card.querySelector(".btn-link");
        infoButton.addEventListener("click", (event) => {
            showCriterionInfo(criterion, event);
        });
        
        rangeInput.addEventListener("input", () => {
            const value = rangeInput.value;

            state.ratings[criterion.id] = value;
            valueDisplay.value = value; // Sync text display
            enableSaveButtonState(true);
            updateThumbStyle(valueDisplay, rangeInput);
            state.ratings_changed = true;
            debounceSaveSurvey(state);
            state.score = calculateScore(state.ratings);
            TitleSelect.updateScore(state.score);

        });
    
        valueDisplay.addEventListener("input", () => {
            const value = clampValue(valueDisplay.value, min=1, max=10);

            state.ratings[criterion.id] = value;
            rangeInput.value = value; // Sync slider
            enableSaveButtonState(true);
            updateThumbStyle(valueDisplay, rangeInput);
            state.ratings_changed = true;
            debounceSaveSurvey(state);
            state.score = calculateScore(state.ratings);
            TitleSelect.updateScore(state.score);
        });
    
        return card;
    }
    
    let saveSurveyTimer = null;

    async function handleSaveButtonClick() {
        // debounceSaveSurvey(state);
        const payload = {
            title_id: state.title_id,
            survey_id: state.survey_id,
            screen_type: state.screen_type,
            ratings: state.ratings,
        };
        // clear the debounce timer if it exists
        if (saveSurveyTimer) clearTimeout(saveSurveyTimer);
        await saveSurveyResponses(payload);
        resetRatingsState(payload.ratings);
        enableSaveButtonState(false, "saved");
    }
    function handleEditButtonClick() {
        resetSurveySearch();
    }
    function handleSearchInput() {
        surveySearch();
    }


    async function debounceSaveSurvey(proposedState) {
        // const saveButton = document.getElementById("save-ratings-button");
    
        if (!proposedState.ratings_changed) {
            console.info("zinny: Save called, but no changes to save.");
            return;
        }
    
        const payload = {
            title_id: proposedState.title_id,
            survey_id: proposedState.survey_id,
            screen_type: proposedState.screen_type,
            ratings: proposedState.ratings,
        };
    
        if (saveSurveyTimer) clearTimeout(saveSurveyTimer);
        saveSurveyTimer = setTimeout(async () => {
            try {
                await saveSurveyResponses(payload);
                resetRatingsState(payload.ratings);
                enableSaveButtonState(false, "auto_saved");
            } catch (error) {
                console.error("zinny: Error saving survey responses:", error);
            }
        }, 5246); // Debounce duration
    }
    
    
    function enableSaveButtonState(enable, label_key=null) {
        const saveButtonMessages = {
            "save": "Save Ratings",
            "saved": "Saved",
            "auto_saved": "Auto Saved",
            "no_title": "No Title",
            "loaded": "Loaded from DB",
            "no_survey": "No Survey",
        }

        const disabled = !enable; // easier to read function call
        const saveButton = document.getElementById("save-ratings-button");
        saveButton.disabled = disabled;
        if (disabled) {
            saveButton.classList.add("disabled");
            if (label_key == null) { label_key = "saved"; }
            saveButton.querySelector("span").textContent = saveButtonMessages[label_key];
        } else {
            saveButton.classList.remove("disabled");
            if (label_key == null) { label_key = "save"; }
            saveButton.querySelector("span").textContent = saveButtonMessages[label_key];
        }
    }
    
    
    async function saveSurveyResponses(payload) {
    
        try {
            const response = await fetch("/api/v1/ratings/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });
    
            if (response.ok) {
                console.info("zinny: Survey responses saved successfully.");
            } else {
                console.error("zinny: Failed to save survey responses.");
            }
        } catch (error) {
            console.error("zinny: Error saving survey responses:", error);
        }
    }
    
    function calculateScore(ratings) {
        if (ratings == null) {
            return "--";
        }
        if (Object.keys(ratings).length === 0) {
            return "--";
        }
        const validRatings = Object.values(ratings)
            .filter((value) => value !== "" && value !== null)
            .map(Number); // Convert strings to numbers
    
        if (validRatings.length === 0) {
            return null; // No valid ratings to calculate mean
        }
    
        const sum = validRatings.reduce((acc, value) => acc + value, 0);
        return sum / validRatings.length;
    }
    
    function calcWeightedMean(ratings, weights) {
        const validRatings = Object.entries(ratings)
            .filter(([key, value]) => value !== "" && value !== null && weights[key] !== undefined)
            .map(([key, value]) => ({ rating: Number(value), weight: weights[key] }));
    
        if (validRatings.length === 0) {
            return null; // No valid ratings to calculate weighted mean
        }
    
        const totalWeightedSum = validRatings.reduce((acc, { rating, weight }) => acc + rating * weight, 0);
        const totalWeights = validRatings.reduce((acc, { weight }) => acc + weight, 0);
    
        score = totalWeightedSum / totalWeights;
        state.score = score;
    }
    

    return {
        // used in HTML:
        handleSearchInput,
        handleEditButtonClick,
        handleSaveButtonClick,
        // used by other js:
        fetchAllSurveys,
        selectSurvey,
        clearSurveyResponses,
        debounceSaveSurvey,
        enableSaveButtonState,
        setCriteriaEditable,
        setupCriteriaInteraction,
        // private functions:
        // createSurveyCard,
        // resetSurveySearch,
        // showCriterionInfo,
        // setupCriterionInteractions,
        // createUniqueId,
        // createCriterionCard,
        // hideCriteriaList,
        // surveySearch,
        // showCriteriaList,
        // saveSurveyResponses,
    };


})();
