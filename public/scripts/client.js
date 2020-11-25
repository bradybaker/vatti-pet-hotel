console.log('js');

$(document).ready(function () {
  console.log('JQ');
  // Establish Click Listeners
  setupClickListeners()
  // Load existing pets on page load
  getPets();

}); // End doc ready

function setupClickListeners() {
<<<<<<< HEAD
  $('#addButton').on('click', function () {
    console.log('in addButton on click');

    // get user input and put in an object
    // NOT WORKING YET :(
    // using a test object
=======
  $( '#addButton' ).on( 'click', function(){
    console.log( 'in addButton on click' );
    // Get user input and put in an object using a test object
>>>>>>> main
    let petToSend = {
      pet: 'testName',
      breed: 'testName',
      color: 'testName',
    };
<<<<<<< HEAD
    // call saveKoala with the new obejct
    savePet(petToSend);
=======
    // Call savePet with the new obejct
    savePet( petToSend );
>>>>>>> main
  });

  $('#viewPets').on('click', '.btn-transferClass', function () {
    petId = $(this).closest('tr').data('id');
    setTransferStatus(petId);
  });

  $('#viewPets').on('click', '.btn-deletePetClass', function () {
    petId = $(this).closest('tr').data('id')
    deletePet(petId);
  });

}

<<<<<<< HEAD


function getPets() {
  console.log('in getPets');
=======
function getPets(){
  console.log( 'in getPets' );
>>>>>>> main
  let html = '';
  $("#viewPets").empty();
  $.ajax({
    type: 'GET',
    url: '/pets'
  }).then(function (response) {
    console.log(response.pets[0][1]);
    // Append data to the DOM
    for (let i = 0; i < response.pets.length; i++) {
      html = `<tr data-id="${response.pets[i][0]}">
                    <td>${response.pets[i][1]}</td>
                    <td>${response.pets[i][2]}</td>
                    <td>${response.pets[i][3]}</td>
                    <td>${response.pets[i][4]}</td>
              `;
      html += `<td>                   
                  <button class="btn-deletePetClass">Delete</button>
                </td>
                <td>                   
                  <button class="btn-changeStatus">Check In</button></td>
                `;
      $('#viewPets').append(html)
    }  // end of for loop
  });
}
// ajax call to server to get koalas

// end getKoalas

function savePet(newPet) {
  console.log('in savePet', newPet);
  // ajax call to server to get koalas
  let payloadObject = {  // these tacos must match those in the router
    name: $('#nameIn').val(),
    breed: $('#breedIn').val(),
    color: $('#ageIn').val(),
  }
  $.ajax({
    type: 'POST',
    url: '/pet',
    data: payloadObject
  }).then(function (response) {
    $('#nameIn').val(''),
      $('#breedIn').val(''),
      $('#colorIn').val(''),
      getPets();
  })
    .catch(function (error) {
      console.log(`Error:`, error);
      alert('Something bad happened')
    });
} // End savePet function

function deletePet(petId) {
  $.ajax({
    method: 'DELETE',
    url: `/pets/${petId}`
  })
    .then(function (response) {
      getPets();
    })
    .catch(function (error) {
      console.log('Error:', error);
      alert('Something bad happened. Try again later');
    })
} // End deletePet function