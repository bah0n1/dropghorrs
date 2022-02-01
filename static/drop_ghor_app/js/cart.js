// var data = 0;
  
//printing default value of data that is 0 in h2 tag
// document.getElementById("counting").innerText = data;
  
//creation of increment function
function increment(id,price) {
    on_data=document.getElementById("counting"+id).textContent;
    data = parseInt(on_data) + 1;
    document.getElementById("counting"+id).innerText = data;
    data=document.getElementById("quentity"+id).value
    on_data=document.getElementById("counting"+id).textContent;
    on_quentity=String(data.split(",")[0])+","+on_data
    data=document.getElementById("quentity"+id)
    data.value=on_quentity
    quentity_price= document.getElementById(id).innerText = price*parseFloat(on_data);
}
//creation of decrement function
function decrement(id,price) {
    on_data=document.getElementById("counting"+id).textContent;
    if (parseInt(on_data)>1) {
        data = on_data - 1;
        document.getElementById("counting"+id).innerText = data;
        data=document.getElementById("quentity"+id).value
        on_data=document.getElementById("counting"+id).textContent;
        on_quentity=String(data.split(",")[0])+","+on_data
        data=document.getElementById("quentity"+id)
        data.value=on_quentity
        quentity_price= document.getElementById(id).innerText = price*parseFloat(on_data);

    }
        
}