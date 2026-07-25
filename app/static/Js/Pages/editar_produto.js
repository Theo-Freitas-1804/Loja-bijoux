document.addEventListener("DOMContentLoaded" , ()=>{
  
  const btninput = document.querySelector("#btn-input-foto")
  const inputfiles = document.querySelector("#fotos")
  
  btninput.addEventListener("click" , ()=>{
    inputfiles.click()
  })
})