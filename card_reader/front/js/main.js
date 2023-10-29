
function getMensalidades(){

    let url = "localhost:8080/api/mensalidades";

    fetch(url)
        .then((response) => response.json)
        .then(mensalidades => {


            let tabela = document.getElementById('table_body');

            mensalidades.array.forEach(element => {
                



            });
            

        })
        
    .catch(e => console.log(e));


}


