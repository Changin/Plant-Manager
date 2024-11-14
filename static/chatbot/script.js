function appendAns(user, answer){
    let card = document.createElement('div');     // card div 태그 생성
    if (user == 'me'){
        card.setAttribute('class', 'card my-3 w-65');
        card.setAttribute('style', 'margin-left: 35%; background-color: honeydew; border-radius: 25px 25px 0px 25px');
    }
    else{
        card.setAttribute('class', 'card my-3 w-75');        // class 지정
        card.setAttribute('style', 'border-radius: 25px 25px 25px 0px')
    }

    let card_body = document.createElement('div');  // card body div 태그 생성
    if (user == 'me'){
        card_body.setAttribute('class', 'card-body text-end');
    }
    else{
        card_body.setAttribute('class', 'card-body');
    }

    // 이름표 넣기
    let nametag = document.createElement('h6');
    nametag.setAttribute('class', 'card-subtitle mb-2 text-muted');
    nametag.innerHTML = user

    // 내용 넣기
    let context = document.createElement('p');  // p 태그 생성
    context.setAttribute('class', 'card-text');
    context.innerHTML = answer;            

    // 태그 계층 완성, 추가
    card_body.appendChild(nametag);
    card_body.appendChild(context);
    card.appendChild(card_body);
    document.getElementById("answer").appendChild(card);

    // 내용 반환
    return context;
}

function query(){
    let plant_serial = document.getElementById("select").value;
    let prompt = document.getElementById("prompt").value;
    document.getElementById("prompt").value = "";
    appendAns('me', prompt);
    

    let reply = appendAns('bot', '입력중...')

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