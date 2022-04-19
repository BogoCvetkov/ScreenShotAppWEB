const login = async function (){
    let response = await fetch( "/api/login/",{
        method:"POST",
        headers: {
            'Content-Type': 'application/json'},
        body: JSON.stringify({
            email:"bogomil@xplora.bgb",
            password:"password"
        })
      })

      response = await response.json()
    console.log(response)
  }

  login()