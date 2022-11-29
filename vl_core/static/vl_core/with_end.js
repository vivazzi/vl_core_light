function with_end(number, array){
    array = array.split('_');
    let result = array[2];
    let i = number % 100;
    if (11 <= number && number <= 19) {
        result = array[2]
    } else {
        i = i % 10;
        if (i === 1) result = array[0];
        if (1 < i && i <= 4) result = array[1];
        if (i > 4) result = array[2];
    }
    return `${number} ${result}`
}