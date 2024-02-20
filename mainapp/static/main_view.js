// Select the main content element in the HTML document
var mainContent = document.querySelector('main');

// Select the loading screen element with the class 'loading-screen'
var loadingScreen = document.querySelector('.loading-screen');

// Select the prompt input box element with the id 'prompt-form'
var promptInputbox = document.getElementById('prompt-form');

// Define a variable for the base URL used for static assets
var staticBaseUrl = "{% static '' %}";

// Function to adjust the height of elements with a specified class to match the height of the tallest element
function justifyHeight(className) {
    // Select all elements with the specified class
    var elements = document.querySelectorAll(className);
    var maxElementHeight = 0;

    // Loop through the selected elements to find the maximum height
    elements.forEach(function (element) {
        var height = element.clientHeight;

        if (height > maxElementHeight) { maxElementHeight = height; }
    });

    // Set the height of all elements to the maximum height found
    elements.forEach(function (element) {
        element.style.height = maxElementHeight + 'px';
    });
}

// Function to handle resizing of the window
function handleResize() {
    // Check if window width is greater than or equal to 1450 pixels
    if (window.innerWidth >= 1450) {
        // Adjust the height of elements with specified classes
        justifyHeight('.title-container');
        justifyHeight('.platforms-container');
    }
}

// Initial call to handleResize function
handleResize();

// Call handleResize function whenever the window is resized
window.addEventListener('resize', handleResize);

// Function to pick a random prompt from a list and submit it
function pickRandomMovies() {
    // Select the form element
    var form = document.getElementById("prompt-form");
    var textField = form.elements["text"];

    // List of random prompts
    const randomPrompts = [
        "Recommend me random movies, different from each other: blockbuster, non US, older than 2010, nostalgic, action in UK.",
        "Recommend me random movies, different from each other: critically acclaimed, comedy, science fiction, animated, from the 80s.",
        "Recommend me random movies, different from each other: classic, thriller, foreign language, post-apocalyptic, based on a true story.",
        "Recommend me random movies, different from each other: indie, fantasy, documentary, set in a dystopian future, directed by a woman.",
        "Recommend me random movies, different from each other: cult classic, horror, musical, black and white, non-linear narrative.",
        "Recommend me random movies, different from each other: mind-bending, romantic, heist, family-friendly, set in a different time period.",
        "Recommend me random movies, different from each other: psychological thriller, historical, coming-of-age, satirical, with a strong female lead.",
        "Recommend me random movies, different from each other: underdog sports, animated, non-English language, biographical, set in a war.",
        "Recommend me random movies, different from each other: suspenseful, neo-noir, Western, directed by a debut filmmaker, based on a book.",
        "Recommend me random movies, different from each other: time travel, comedy-drama, crime, space exploration, directed by a person of color.",
        "Recommend me random movies, different from each other: thought-provoking, musical comedy, documentary series, set in a futuristic world, non-linear narrative.",
        "Recommend me random movies, different from each other: cult classic, teen romance, martial arts, animated, with a strong environmental message.",
        "Recommend me random movies, different from each other: mystery, classic Hollywood, psychological horror, non-English language, based on mythology.",
        "Recommend me random movies, different from each other: dark comedy, war film, biographical, futuristic, set in a small town.",
        "Recommend me random movies, different from each other: courtroom drama, animated fantasy, spy thriller, non-US, based on a graphic novel.",
        "Recommend me random movies, different from each other: feel-good, dystopian, action comedy, romantic drama, directed by a famous actor-turned-director.",
        "Recommend me random movies, different from each other: thought-provoking science fiction, fantasy adventure, animated musical, non-English language, based on folklore.",
        "Recommend me random movies, different from each other: cyberpunk, historical romance, crime thriller, documentary series, set in the future.",
        "Recommend me random movies, different from each other: superhero, mockumentary, coming-of-age drama, space opera, directed by a female filmmaker.",
        "Recommend me random movies, different from each other: political satire, animated comedy, horror anthology, biographical drama, set in a post-war era.", "I like Ryan Gosling",
        "Some thriller from Sweden",
        "I enjoy superhero movies, but don't like Marvel",
        "Horror produced before 1980",
        "Snowy movie, but not about Christmas",
        "Give me a romantic comedy with Sandra Bullock",
        "I'm into historical dramas set in ancient Rome",
        "Recommend a mind-bending science fiction film similar to Inception",
        "Looking for a fantasy movie with dragons, but not Game of Thrones",
        "A family-friendly animated film with talking animals",
        "Find me a crime thriller set in a futuristic dystopian world",
        "I want a classic black and white film, preferably a mystery",
        "Suggest a war movie based on a true story",
        "I enjoy Quentin Tarantino films, recommend something similar",
        "Give me a feel-good movie with a strong female lead",
        "Looking for a documentary about space exploration",
        "I'm in the mood for a foreign language film any genre",
        "Recommend a comedy that doesn't rely on slapstick humor",
        "A psychological horror film that's not too intense",
        "I love Christopher Nolan's work, suggest a non-Batman film",
        "Find me a crime documentary that explores unsolved mysteries",
        "I want a coming-of-age film set in the 80s",
        "Give me an action-packed movie with a strong ensemble cast",
        "A lighthearted fantasy film suitable for a family movie night",
        "Recommend a western movie with a modern twist", "Fantasy adventure with magical creatures", "Biography of a famous scientist or inventor",
        "Sci-fi comedy with aliens",
        "Film adaptation of a classic book", "Romantic Victorian-era period piece",
        "Funny road trip movie with friends",
        "Thought-provoking political drama", 'Movie worse than "The Room"', "Something where Sean Bean character doesn't die", 'Classical Christmas movie, like "Die Hard"', "Main character is bald and angry",
        "I'm a fan of low-budget Iranian bean shelling dramas type movies",
        "Spaghetti westerns from 60s",
        "It is Halloween today, recommend me something to watch",
        "Me and my girlfriend love Asian horrors", "I feel nostalgic",
        "I am in night drive mood",
        "I need some motivation", "I love Tim Burton's 'Beetle Juice'",
        "I am a fan of David Lynch films, recommend something similiar",
    ];

    // Generate a random index to pick a prompt from the list
    const randomIndex = Math.floor(Math.random() * randomPrompts.length);
    const pickedPrompt = randomPrompts[randomIndex];

    // Set the value of the text field to the picked prompt and submit the form
    textField.value = pickedPrompt;
    form.submit();
    textField.value = "";

    // Hide main content, prompt input box, and display loading screen
    mainContent.style.display = 'none';
    promptInputbox.style.display = 'none';
    loadingScreen.style.display = 'flex';
}

// Function to display the loading screen by hiding main content and prompt input box
function displayLoadingScreen() {
    mainContent.style.display = 'none';
    promptInputbox.style.display = 'none';
    loadingScreen.style.display = 'flex';
}

// Function to show a tooltip at a specified position
function showTooltip(tooltip, translateX) {
    var tooltip = document.getElementById(tooltip);
    tooltip.style.transform = "translateY(-195%) translateX(" + translateX + ") scale(1)";
}

// Function to hide a tooltip at a specified position
function hideTooltip(tooltip, translateX) {
    var tooltip = document.getElementById(tooltip);
    tooltip.style.transform = "translateY(-195%) translateX(" + translateX + ") scale(0)";
}

// List of prompt examples
const promptIdea = document.querySelector(".prompt-examples");
promptIdeasList = ["I like Ryan Gosling",
    "Some thriller from Sweden",
    "I enjoy superhero movies, but don't like Marvel",
    "Horror produced before 1980",
    "Snowy movie, but not about Christmas",
    "I feel nostalgic",
    "I am in night drive mood",
    "I need some motivation",
    "I love Tim Burton's 'Beetle Juice'",
    "Movie where Keanu Reeves character is happy",
    "I am a fan of David Lynch films, recommend something similiar",
    "I like Jim Carrey, but I'm not in the mood for comedies",
    "Movie starring Mark Wahlberg or Matt Damon",
    "Give me a romantic comedy with Sandra Bullock",
    "I'm into historical dramas set in ancient Rome",
    "Recommend a mind-bending science fiction film similar to Inception",
    "I'm a fan of low-budget Iranian bean shelling dramas type movies",
    "Spaghetti westerns from 60s",
    "It is Halloween today, recommend me something to watch",
    "Me and my girlfriend love Asian horrors",
    "Looking for a fantasy movie with dragons, but not Game of Thrones",
    "A family-friendly animated film with talking animals",
    "Find me a crime thriller set in a futuristic dystopian world",
    "I want a classic black and white film, preferably a mystery",
    "Suggest a war movie based on a true story",
    "I enjoy Quentin Tarantino, but already watched all of his movies 10 times",
    "Give me a feel-good movie with a strong female lead",
    "Looking for a documentary about space exploration",
    "I'm in the mood for a foreign language film, any genre",
    "Recommend a comedy that doesn't rely on slapstick humor",
    "A psychological horror film that's not too intense",
    "I love Christopher Nolan's work, suggest a non-Batman film",
    "Find me a crime documentary that explores unsolved mysteries",
    "I want a coming-of-age film set in the 80s",
    "Give me an action-packed movie with a strong ensemble cast",
    "A lighthearted fantasy film suitable for a family movie night",
    "Recommend a western movie with a modern twist", "Fantasy adventure with magical creatures", "Biography of a famous scientist or inventor",
    "Sci-fi comedy with aliens",
    "Film adaptation of a classic book", "Romantic Victorian-era period piece",
    "Funny road trip movie with friends",
    "Thought-provoking political drama", 'Movie worse than "The Room"', "Something where Sean Bean character doesn't die", 'Classical Christmas movie, like "Die Hard"', "Main character is bald and angry"];
colorsList = ['rgb(255,255,0)', 'rgb(0,255,255)', 'rgb(0,255,0)', 'rgb(255,0,205)', 'rgb(5,99,244)'];
let currentIndex = -1;

// Function to animate typing of prompt examples
function typingAnimation(index) {
    // Wait for 1 second before running the rest of the function
    setTimeout(() => {
        // Check if index is less than 100
        if (index < 100) {
            // Check if promptIdea is not null
            if (promptIdea !== null) {
                // Select a random prompt example
                var selectedIdea = promptIdeasList[Math.floor(Math.random() * promptIdeasList.length)];
                currentIndex = (currentIndex + 1) % colorsList.length;
                promptIdea.style.color = colorsList[currentIndex];
                promptIdea.style.textShadow = " 0 0 1px 3px" + colorsList[currentIndex];
                let word = "";
                // Loop through the characters of the selected prompt
                for (let i = 0; i < selectedIdea.length; i++) {
                    setTimeout(() => {
                        word += selectedIdea[i];
                        promptIdea.innerHTML = word + "<span class='cursor'>|</span>";

                        // Check if it's the last iteration of the first loop
                        if (i === selectedIdea.length - 1) {
                            // Pause for 1 second before starting the second loop
                            setTimeout(() => {
                                // Second loop: Delete the text
                                for (let j = selectedIdea.length - 1; j >= 0; j--) {
                                    setTimeout(() => {
                                        word = word.substring(0, j);
                                        promptIdea.innerHTML = word + "<span class='cursor'>|</span>";
                                    }, 20 * (selectedIdea.length - j));
                                }
                                // Run the next iteration after the second loop is completed
                                setTimeout(() => {
                                    typingAnimation(index + 1);
                                }, 30 * i + 500);
                            }, 1000); // Pause for 1 second
                        }
                    }, 30 * i);
                }
            }
        }
    }, 1000); // Wait for 1 second
}

// Start the typing animation
typingAnimation(0);

// Function to show full streaming info on button click
function showFullStreaming() {
    const buttons = document.querySelectorAll(".show-streaming");
    const streamingInfoContainer = document.querySelectorAll(".full-streaming-info");
    const resultsContainer = document.querySelector(".results-container");

    buttons.forEach((button, index) => {
        button.addEventListener("click", () => {
            streamingInfoContainer[index].style.transform = "translateY(10%) scale(1)";
            resultsContainer.style.opacity = "50%";
        });
    });
}

// Function to hide full streaming info on button click
function hideFullStreaming() {
    const buttons = document.querySelectorAll(".close-dial");
    const streamingInfoContainer = document.querySelectorAll(".full-streaming-info");
    const resultsContainer = document.querySelector(".results-container");

    buttons.forEach((button, index) => {
        button.addEventListener("click", () => {
            streamingInfoContainer[index].style.transform = "translateY(10%) scale(0)";
            resultsContainer.style.opacity = "100%";
        });
    });
}

// Call the functions to show and hide full streaming info
showFullStreaming();
hideFullStreaming();