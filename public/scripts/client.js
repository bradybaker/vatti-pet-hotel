console.log( 'js' );
 
$( document ).ready( function(){
  console.log( 'JQ' );
  // Establish Click Listeners
  setupClickListeners()
  // load existing koalas on page load
  getPets();

}); // end doc ready

function setupClickListeners() {
  $( '#addButton' ).on( 'click', function(){
    console.log( 'in addButton on click' );
    
    // get user input and put in an object
    // NOT WORKING YET :(
    // using a test object
    let petToSend = {
      pet: 'testName',
      breed: 'testName',
      color: 'testName',
    };
    // call saveKoala with the new obejct
    savePet( petToSend );
  });
  
  $('#viewPets').on ('click', '.btn-transferClass', function () {
    petId = $(this).closest('tr').data('id');
    setTransferStatus (petId);
  });

  $('#viewPets').on ('click', '.btn-deletePetClass', function () {
    petId = $(this).closest('tr').data('id')
    deletePet (petId);
  });

}



function getPets(){
  console.log( 'in getPets' );
  let html = '';
  $("#viewPets").empty();
  $.ajax({
    type: 'GET',
    url: '/pets'
  }).then(function (response) {
    console.log(response);
    // append data to the DOM
    for (let i = 0; i < response.length; i++) {
      html = `<tr data-id="${response[i].id}">
                    <td>${response[i].pet}</td>
                    <td>${response[i].breed}</td>
                    <td>${response[i].color}</td>
                    <td>${response[i].checked_in}</td>
              `;
      html += `<td>                   
                  <button class="btn-deletePetClass">Delete</button>
                </td>
                `;
      $('#viewPet').append(html)
      }  // end of for loop
  });
}
  // ajax call to server to get koalas
  
 // end getKoalas

function savePet( newPet ){
  console.log( 'in savePet', newPet );
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
    }).then( function (response) {
        $('#nameIn').val(''),
        $('#breedIn').val(''),
        $('#colorIn').val(''),
        getPets();
    })
    .catch ( function (error){
        console.log (`Error:`, error);
        alert ('Something bad happened')
    });
}


function deletePet( petId ) {
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
}