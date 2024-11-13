function appendAns(answer){
    let card = document.createElement('div');     // div 태그 생성
    card.setAttribute('class', 'card my-3');        // class 지정

    let card_body = document.createElement('div'); // div 태그 생성
    card_body.setAttribute('class', 'card-body');      // class 지정
    card_body.innerHTML = answer;                   // 응답 넣기

    // card에 card_body 태그 넣기
    card.appendChild(card_body);
	
    document.getElementById("answer").appendChild(card);
    return card_body;
}

function appendPrompt(prompt){
    let card = appendAns(prompt);
    card.setAttribute('class', 'card-body text-end');

    let nametag = document.createElement('div');
    nametag.setAttribute('class', 'd-flex justify-content-end');

    let name = document.createElement('div');
    name.setAttribute('class', 'badge bg-light text-dark p-2');
    name.innerHTML = 'me'

    nametag.appendChild(name);
    card.appendChild(nametag);
}

function query(){
    let plant_serial = document.getElementById("select").value;
    let prompt = document.getElementById("prompt").value;
    appendPrompt(prompt);

    let reply = appendAns('입력중...')

    const api = '/chatbot/get_response/?serial='+plant_serial+'&prompt='+prompt+'/'

    $.ajax({
        type: 'GET',
        url: api,
        data: {},
        success: (res) => {
            // answer.innerHTML = res['answer']
            // appendAns(res['answer'])
            reply.innerHTML = res['answer']
        }
    });
}