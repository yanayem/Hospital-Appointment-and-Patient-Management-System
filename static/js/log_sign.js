
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const signupFields = document.getElementById('signup-fields');
const userTypeButtons = signupForm.querySelectorAll('.user-type-select button');
let selectedType = 'patient';

function showLogin(){ loginForm.classList.add('active'); signupForm.classList.remove('active'); }
function showSignup(){ signupForm.classList.add('active'); loginForm.classList.remove('active'); }
function togglePassword(id){ const input=document.getElementById(id); input.type = input.type==='password'?'text':'password'; }
function forgotPassword(){ alert('Redirect to forgot password page.'); }

const fields = {
  patient:[[{label:'First Name',type:'text',id:'first-name'},{label:'Last Name',type:'text',id:'last-name'}],[{label:'Email',type:'email',id:'email'},{label:'Mobile',type:'tel',id:'mobile'}],[{label:'NID (Optional)',type:'text',id:'nid'},{label:'Date of Birth',type:'date',id:'dob'}],[{label:'Address',type:'text',id:'address'}],[{label:'Gender',type:'select',id:'gender',options:['Male','Female','Other']},{label:'Password',type:'password',id:'password'},{label:'Confirm Password',type:'password',id:'confirm-password'}]],
  doctor:[[{label:'First Name',type:'text',id:'first-name'},{label:'Last Name',type:'text',id:'last-name'}],[{label:'Email',type:'email',id:'email'},{label:'Mobile',type:'tel',id:'mobile'}],[{label:'NID (Optional)',type:'text',id:'nid'},{label:'Date of Birth',type:'date',id:'dob'}],[{label:'Specialization',type:'text',id:'specialization'},{label:'Degree',type:'text',id:'degree'}],[{label:'Gender',type:'select',id:'gender',options:['Male','Female','Other']},{label:'Password',type:'password',id:'password'},{label:'Confirm Password',type:'password',id:'confirm-password'}]],
  admin:[[ {label:'First Name',type:'text',id:'first-name'},{label:'Last Name',type:'text',id:'last-name'}],[{label:'Email',type:'email',id:'email'},{label:'Mobile',type:'tel',id:'mobile'}],[{label:'Address',type:'text',id:'address'}],[{label:'Gender',type:'select',id:'gender',options:['Male','Female','Other']},{label:'Password',type:'password',id:'password'},{label:'Confirm Password',type:'password',id:'confirm-password'}]]
};

function renderSignup(type){
  signupFields.innerHTML='';
  fields[type].forEach(row=>{
    const rowDiv=document.createElement('div'); rowDiv.className='row';
    row.forEach(f=>{
      const group=document.createElement('div'); group.className='input-group';
      const label=document.createElement('label'); label.innerText=f.label; label.htmlFor=f.id; group.appendChild(label);
      let input;
      if(f.type==='select'){ input=document.createElement('select'); input.id=f.id; input.required=true;
        const defaultOption=document.createElement('option'); defaultOption.value=''; defaultOption.text='Select'; input.appendChild(defaultOption);
        f.options.forEach(opt=>{const option=document.createElement('option'); option.value=opt.toLowerCase(); option.text=opt; input.appendChild(option);});
      } else { input=document.createElement('input'); input.type=f.type; input.id=f.id; input.placeholder=f.label; if(f.type!=='password') input.required=true;}
      if(f.type==='password'){ const wrapper=document.createElement('div'); wrapper.className='password-wrapper'; wrapper.appendChild(input); const eye=document.createElement('span'); eye.className='toggle-password'; eye.innerHTML='&#128065;'; eye.onclick=()=>{input.type=input.type==='password'?'text':'password';}; wrapper.appendChild(eye); group.appendChild(wrapper);}
      else{group.appendChild(input);}
      rowDiv.appendChild(group);
    });
    signupFields.appendChild(rowDiv);
  });
}

userTypeButtons.forEach(btn=>{
  btn.addEventListener('click',()=>{
    userTypeButtons.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active'); selectedType=btn.dataset.type; renderSignup(selectedType);
  });
});

renderSignup(selectedType);

function submitLogin(e){ e.preventDefault(); const email=document.getElementById('login-email').value; const pass=document.getElementById('login-password').value; console.log("Login Data:",{email,pass}); alert('Login submitted! Check console.'); }
function submitSignup(e){ e.preventDefault(); const data={}; fields[selectedType].flat().forEach(f=>{ const el=document.getElementById(f.id); data[f.id]=el?el.value:'';}); console.log("Signup Data:",selectedType,data); alert('Registration submitted! Check console.'); }
