let btns = document.querySelectorAll("[topic]");

for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener('mouseover', function(){
    btns[i].style.backgroundColor = 'gray';
  });
  btns[i].addEventListener('hover', function () {
    btns[i].style.backgroundColor = 'gray';
  });

  btns[i].addEventListener('mouseout', function (){
    btns[i].style.backgroundColor = 'salmon';
    });
    
}

let btn = document.querySelector("#btn-submit");


btn.addEventListener('mouseover', function(){
  btn.style.backgroundColor = '#a1e2a5';
});
btn.addEventListener('hover', function () {
  btn.style.backgroundColor = '#a1e2a5';
});

btn.addEventListener('mouseout', function (){
  btn.style.backgroundColor = 'aliceblue';
  });
    