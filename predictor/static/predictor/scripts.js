function submitForm() {
    const formData = new FormData();
    formData.append('Gender', document.getElementById('Gender').value);
    formData.append('Weight', document.getElementById('Weight').value);
    formData.append('BMI', document.getElementById('BMI').value);
    formData.append('Height', document.getElementById('Height').value);
    formData.append('Age', document.getElementById('Age').value);
    formData.append('BMIcase', document.getElementById('BMIcase').value);
    console.log(formData);

    fetch('/predictor/predict/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = 'Predicted Exercise Recommendation Plan: ' + data.prediction;
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
