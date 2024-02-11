
var mainContent = document.querySelector('main');
var loadingScreen = document.querySelector('.loading-screen');
var promptInputbox = document.getElementById('prompt-form');
var staticBaseUrl = "{% static '' %}";

function justifyHeight(className) {

    console.log("function ran")
    var elements = document.querySelectorAll(className);
    console.log(elements)
    var maxElementHeight = 0;

    elements.forEach(function (element) {
        var height = element.clientHeight;

        if (height > maxElementHeight) { maxElementHeight = height; }
    });

    elements.forEach(function (element) {
        element.style.height = maxElementHeight + 'px';
    });
}


function handleResize() {
    if (window.innerWidth >= 1450) {
        justifyHeight('.title-container');
        justifyHeight('.platforms-container');
    }
}

// Initial call
handleResize();

// Real time resizing
window.addEventListener('resize', handleResize)

function pickRandomMovies() {
    var form = document.getElementById("prompt-form");
    var textField = form.elements["text"];
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
        "Thriller directed by a woman",
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
        "I'm in the mood for a foreign language film with subtitles, any genre",
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
        "Thought-provoking political drama", 'Movie worse than "The Room"', "Something where Sean Bean character doesn't die", 'Classical Christmas movie, like "Die Hard"', "Main character is bald and angry"
    ]
    const randomIndex = Math.floor(Math.random() * randomPrompts.length);
    const pickedPrompt = randomPrompts[randomIndex];

    textField.value = pickedPrompt;
    form.submit();
    textField.value = ""


    mainContent.style.display = 'none'
    promptInputbox.style.display = 'none'
    loadingScreen.style.display = 'flex'

}

function displayLoadingScreen() {
    mainContent.style.display = 'none'
    promptInputbox.style.display = 'none'
    loadingScreen.style.display = 'flex'

}

function toggleImageF(platform, img_off, img_on) {

    var imageElement = platform;
    var checkboxElement = imageElement.nextElementSibling;
    var currentImageIndex = parseInt(imageElement.getAttribute('clicked'));
    var imagePaths = [
        staticBaseUrl + img_off,
        staticBaseUrl + img_on
    ];

    currentImageIndex = (currentImageIndex === 0) ? 1 : 0;
    imageElement.src = imagePaths[currentImageIndex];

    if (checkboxElement && checkboxElement.type === 'checkbox') {
        checkboxElement.checked = (currentImageIndex === 1);
    }
    imageElement.setAttribute('clicked', String(currentImageIndex));
}

function showTooltip(tooltip, translateX) {
    var tooltip = document.getElementById(tooltip);
    tooltip.style.transform = "translateY(-195%) translateX(" + translateX + ") scale(1)";

}

function hideTooltip(tooltip, translateX) {
    var tooltip = document.getElementById(tooltip);

    tooltip.style.transform = "translateY(-195%) translateX(" + translateX + ") scale(0)";
}

const promptIdea = document.querySelector(".prompt-examples");

promptIdeasList = ["I like Ryan Gosling",
    "Some thriller from Sweden",
    "I enjoy superhero movies, but don't like Marvel",
    "Horror produced before 1980",
    "Thriller directed by a woman",
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
    "I'm in the mood for a foreign language film with subtitles, any genre",
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
    "Thought-provoking political drama", 'Movie worse than "The Room"', "Something where Sean Bean character doesn't die", 'Classical Christmas movie, like "Die Hard"', "Main character is bald and angry"]

colorsList = ['rgb(255,255,0)', 'rgb(0,255,255)', 'rgb(0,255,0)', 'rgb(255,0,205)', 'rgb(5,99,244)']

let currentIndex = 0;

setInterval(() => {
    if (promptIdea !== null) {
        var selectedIdea = promptIdeasList[Math.floor(Math.random() * promptIdeasList.length)];
        promptIdea.textContent = selectedIdea;
        currentIndex = (currentIndex + 1) % colorsList.length;
        promptIdea.style.color = colorsList[currentIndex];
    }
}, 1000);