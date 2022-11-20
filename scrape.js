const category = document.querySelectorAll('yt-chip-cloud-chip-renderer') // NodeList
const categoryArray = Array.from(category) // List Array

categoryTextArray = [];
categoryArray.forEach(function(ele){
    test.push(ele.innerText);
})

// Get a click event on each and every category
categoryArray.forEach(function(ele){
    ele.addEventListener('click', getMovieCount(ele))
})

// Get movie count
titles = []
function getMovieCount(ele){
    titlesElements = document.querySelectorAll('style-scope ytd-rich-grid-media')
    titles.push(titlesElements.innerText)
    titlesArray = Array.from(titles)

    // Get count of Elements
    lengthOfTitle = titlesArray.length
}