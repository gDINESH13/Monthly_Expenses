


document.addEventListener('DOMContentLoaded',load);

function load()
{
	
    try{
        document.querySelector('#ReportButton');
        document.querySelectorAll('#ReportButton').forEach(but=>{

			but.addEventListener('click',event=>Report(but));
			//but.onclick=()=>{ alert(`${but.className}`) }
		});
        
    }
    catch(err)
    {
        console.log("Error",err)
    }
}

function Report(but){
    date=but.getAttribute('data-date');
    alert(`${date}`);
    console.log('hii');
    //fetch(`/pieChart/${m}`,{
    //    method:'POST',
    //    
    //    body:JSON.stringify({
    //        new_text:new_text
    //    })
    //})
    //.then(response=>response.json())
    //.then(result=>{
    //    console.log(result);
    //})
}