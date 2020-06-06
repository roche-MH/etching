const output_ready = false
const result = document.querySelector(".FC_result");
const btn = document.querySelector(".FC_processBtn");

function processStart() {
    const output_ready = true;
    console.log(output_ready);
    outputPrint(output_ready);
}

function outputPrint(output_ready) {
    if( output_ready == true ){
        console.log('결과물 출력');
    } else {
        console.log('결과물 출력 안함');
    };
}