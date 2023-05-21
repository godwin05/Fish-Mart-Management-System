var iter = document.querySelectorAll('.bar').length
for (var i=0;i<iter;i++){
    
    document.querySelectorAll('.bar')[i].addEventListener('click',function(){
    var id=this.innerHTML;
    console.log(id)
    var active_btn = document.querySelector('#drop-down');
    var search_btn = document.querySelector('.search');
    var account = document.querySelector('.user-data');
    console.log(id);
    if (id==='Registration <i class="fa-solid fa-circle-chevron-down"></i>'){
        console.log("truee");
        active_btn.style.display='block';
        // setTimeout(function(){
        //     active_btn.style.display='none';
        // },3000);
        search_btn.style.display='none';
        account.style.display='none';
        
    }else if(id === 'search &nbsp;<i class="fa-solid fa-magnifying-glass"></i>'){
        console.log("searc true..");
        search_btn.style.display='block';
        active_btn.style.display='none';
        account.style.display='none';
    }else if(id === 'Account'){
        console.log("acc true");
        account.style.display='block';
        active_btn.style.display='none';
        search_btn.style.display='none';
    }
    else{
        active_btn.style.display='none';
        search_btn.style.display='none';
        account.style.display='none';
    }
});
}