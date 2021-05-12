const BASE_URL = "http://127.0.0.1:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
        <div class="m-2 card text-center" data-cupcake-id=${cupcake.id}>
            <div class="card-body">
                <img class="card-img-top img-fluid" style="height: 200px" src="${cupcake.image}">
                <h5 classs="card-title">Flavor: ${cupcake.flavor}</h5>
                <h5 classs="card-title">Size: ${cupcake.size}</h5>
                <h5 classs="card-title">Rating: ${cupcake.rating}</h5>
                <button class="delete btn btn-danger">Delete</button>
            </div>
        </div>
    `;
}


$('#cupcake-form').on("submit", async function(e) {
    e.preventDefault()

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const res = await axios.post(`${BASE_URL}/cupcakes`, {flavor, rating, size, image});

    let cupcake = $(generateCupcakeHTML(res.data.cupcake));
    $("#cupcakes-list").append(cupcake);
    $("#cupcake-form").trigger("reset");
})

async function showCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let data of response.data.cupcakes)
    {
        let newCupcake = $(generateCupcakeHTML(data));
        $("#cupcakes-list").append(newCupcake);
    }
}

$('#cupcakes-list').on("click", ".delete", async function(e) {
    let cupcake = $(e.target).closest(".card");
    let cupcakeId = cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    cupcake.remove();
})


$(showCupcakes);