function test(){
    console.log("Running")
    const el = document.querySelector(".test")

    const source= new EventSource("http://127.0.0.1:8080/stream")
    source.addEventListener("greeting",(event)=>{
        let data = JSON.parse(event.data)
        let newEl = document.createElement("div")
        newEl.textContent = data.message
    },false)
    source.addEventListener("error", (event)=>{
        alert("Something wrong happened while streaming")
    },false)
}


test()

