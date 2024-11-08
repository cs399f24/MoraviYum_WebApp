var dropdown_button1 = document.getElementById("activateDropdown1")
var dropdown_button2 = document.getElementById("activateDropdown2")
var profileimg = document.getElementById("image_container2")
var logout_button = document.getElementById("logout_button_container")

var dropdown1 = document.getElementById("dropdown1")
var dropdown2 = document.getElementById("dropdown2")

dropdown_button1.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'block';
})

dropdown_button1.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'none';
});

dropdown_button2.addEventListener('mouseover', () =>{
    console.log('clicked2')
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'block';
})

dropdown_button2.addEventListener('mouseleave', () => {
    console.log('left hover2');
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'none';
})

dropdown1.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'block';
})

dropdown1.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown1');
    dropdown.style.display = 'none';
})

dropdown2.addEventListener('mouseover', () => {
    console.log('hovered')
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'block';
})

dropdown2.addEventListener('mouseleave', () => {
    console.log('left hover');
    const dropdown = document.getElementById('dropdown2');
    dropdown.style.display = 'none';
})

// Array to hold review data
const reviews = [];

// Function to display reviews in the review list
function displayReviews() {
    const reviewList = document.getElementById('review_list');
    reviewList.innerHTML = ''; // Clear existing reviews

    // Loop through the reviews array and create list items
    reviews.forEach((review) => {
        const reviewItem = document.createElement('div');
        reviewItem.classList.add('review-item');
        reviewItem.innerHTML = `
            <strong>User ID:</strong> ${review.user_id}<br>
            <strong>Food ID:</strong> ${review.food_id}<br>
            <strong>Rating:</strong> ${review.rating}<br>
            <strong>Review:</strong> ${review.review}<br>
            <strong>Time:</strong> ${review.time_stamp}
        `; // Format the review information
        reviewList.appendChild(reviewItem); // Add review to the list
    });
}

// Add event listener to the button for showing the review form
document.getElementById('show_review_form').addEventListener('click', () => {
    document.getElementById('reviewForm').style.display = 'block'; // Show the form
});

// Add event listener to the form for submitting a new review
document.getElementById('reviewForm').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Gather form data
    const user_id = document.getElementById('user_id').value;
    const food = document.getElementById('food').value;
    const rating = parseInt(document.getElementById('rating').value);
    const review_text = document.getElementById('review_text').value;

    // Create a new review object
    const newReview = {
        user_id: user_id,
        food: food,
        rating: rating,
        review: review_text
    };

    // Make a POST request to submit the review
    fetch('/submit_review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newReview)})
        .then(data => {
            document.getElementById('reviewForm').reset();
            document.getElementById('reviewForm').style.display = 'none';
    })
});

document.addEventListener('DOMContentLoaded', () => {
    // Fetch reviews when the page loads
    fetch('/get_reviews')
        .then(response => response.json())
        .then(reviews => {
            populateReviewTable(reviews);
        })
        .catch(error => console.error('Error fetching reviews:', error));
});

// Function to populate the review table
function populateReviewTable(reviews) {
    const reviewList = document.getElementById('review_list');

    // table element
    const table = document.createElement('table');
    table.classList.add('review-table');

    // table header
    const headerRow = document.createElement('tr');
    const headers = ['User ID', 'Food', 'Rating', 'Review', 'Timestamp'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);

    // Populate the table rows with review data
    reviews.forEach(review => {
        const row = document.createElement('tr');

        // Create table cells for each piece of data
        const userIdCell = document.createElement('td');
        userIdCell.textContent = review.user_id;
        row.appendChild(userIdCell);

        const foodIdCell = document.createElement('td');
        foodIdCell.textContent = review.food_id;
        row.appendChild(foodIdCell);

        const ratingCell = document.createElement('td');
        ratingCell.textContent = review.rating;
        row.appendChild(ratingCell);

        const reviewCell = document.createElement('td');
        reviewCell.textContent = review.review;
        row.appendChild(reviewCell);

        const timeStampCell = document.createElement('td');
        timeStampCell.textContent = review.time_stamp;
        row.appendChild(timeStampCell);

        // Append the row to the table
        table.appendChild(row);
    });

    reviewList.appendChild(table);
}

/*profileimg.addEventListener('click', () => {
    console.log("clicked the img")
    logout_button.style.display = 'block';
})

logout_button.addEventListener('mouseover', () => {
    logout_button.style.display = 'block';
})

logout_button.addEventListener('click', () => {
    const BASE_URL = window.location.origin
    window.location.href = BASE_URL + '/logout';
})
profileimg.addEventListener('mouseleave', () => {
    logout_button.style.display = 'none';
})*/

