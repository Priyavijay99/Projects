fetch('./s.json')
.then(function(response){
	return response.json();
})
.then(function(data){

	var col = [];

            for (var key in data[0]) {
                    col.push(key);
            }
    col.push("Action")
    console.log(col)
     var table = document.createElement("table");
     table.id = "myTable"
     var tr = table.insertRow();

     for (var i = 0; i < col.length; i++) {
            var th = document.createElement("th");   
            th.innerHTML = col[i];
            tr.appendChild(th);
        }
     for (var i = 0; i < data.length; i++) {

            tr = table.insertRow();
            tr.id="row_"+i;

            for (var j = 0; j < col.length; j++) {
                var tabCell = tr.insertCell();
                // tabCell.innerHTML = "Hello";
                if (data[i][col[j]]==undefined){
                    
                   // tabCell.innerHTML = "<button>Delete</button>";
                    var btn=document.createElement("Button")
                    
                    btn.innerHTML="Delete";
                    btn.id = tr.id
                    
                    tabCell.appendChild(btn);
                    btn.onclick=function(e){
                        rowid = e.target.id
                        // document.getElementById("myTable").deleteRow(remtr);
                        var row = document.getElementById(rowid);
                        row.parentNode.removeChild(row);
                        // remtr.parentNode.removeChild(remtr);
                    };
                }
                else{
                    tabCell.innerHTML = data[i][col[j]];
                }
            }
        }
        var divContainer = document.getElementById("showData");
        divContainer.appendChild(table);

});

// function del_tr(remtr){
//     console.log("Hello")
//     console.log("row id", remtr.id)
//     remtr.parentNode.removeChild(remtr);
//     return false;
// }