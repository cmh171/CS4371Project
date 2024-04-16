/**
 * We use a basic hill cipher for encryption/decryption
 * It's not a good encryption, but it's meant to showcase our strategy.
 * It's also not entirely simplistic.
 */

function int_to_letter(i) {
    if (i < 0) i += 26;
    let int_obj = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',
        7: 'H',
        8: 'I',
        9: 'J',
        10: 'K',
        11: 'L',
        12: 'M',
        13: 'N',
        14: 'O',
        15: 'P',
        16: 'Q',
        17: 'R',
        18: 'S',
        19: 'T',
        20: 'U',
        21: 'V',
        22: 'W',
        23: 'X',
        24: 'Y',
        25: 'Z'
    }
    return int_obj[Number(i)];
}


function letter_to_int(letter) {
    let letter_obj = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
        'K': 10,
        'L': 11,
        'M': 12,
        'N': 13,
        'O': 14,
        'P': 15,
        'Q': 16,
        'R': 17,
        'S': 18,
        'T': 19,
        'U': 20,
        'V': 21,
        'W': 22,
        'X': 23,
        'Y': 24,
        'Z': 25
    }
    return letter_obj[letter]
}


function extended_euclidean_algorithm(a, b) {
    if (a === 0) {
        return [b, 0, 1];
    }
    else {
        let [gcd, x2, x1] = extended_euclidean_algorithm(b % a, a);
        let q = Math.floor(b / a);
        let x = x1 - q * x2;
        return [gcd, x, x2];
    }
}

function mult_inverse(det, mod) {
    while (det < mod)
        det += mod;
    let [gcd, x, _] = extended_euclidean_algorithm(det, mod);
    if (gcd != 1) {
        console.error("INVALID GCD!!!");
    }
    else return x % mod;
}

function upper_and_replace(text) {
    text = text.toUpperCase().replace(' ', '');
    return text;
}

function determinant(key2d) {
    let det = (key2d[0][0] * key2d[1][1]) - (key2d[1][0] * key2d[0][1]);
    return det;
}

function key_inverse(mult_inverse, adj) {
    let temp = [[adj[0][0] % 26, adj[0][1] % 26], [adj[1][0] % 26, adj[1][1] % 26]];
    let k_prep = [[temp[0][0] * mult_inverse, temp[0][1] * mult_inverse], [temp[1][0] * mult_inverse, temp[1][1] * mult_inverse]];
    let k_inverse = [[k_prep[0][0] % 26, k_prep[0][1] % 26], [k_prep[1][0] % 26, k_prep[1][1] % 26]];

    return k_inverse;
}

function cipher_decryption(cipher, key) {
    let msg_matrices = [];
    
    
    for (let i = 0; i < cipher.length; i += 2) {
        matrix = [letter_to_int(cipher[i]), letter_to_int(cipher[i + 1])];
        msg_matrices.push(matrix);
    }


    if (key.length > 4) key = key.slice(0, 4);
    key = upper_and_replace(key);
    //console.log(key);
    let key2d = [[letter_to_int(key[0]), letter_to_int(key[2])], [letter_to_int(key[1]), letter_to_int(key[3])]];

    let det = determinant(key2d);
    
    let inverse = mult_inverse(det, 26);

    let adj = [[key2d[1][1], -key2d[0][1]], [-key2d[1][0], key2d[0][0]]];

    let k_inverse = key_inverse(inverse, adj);

    let decrypted_text = "";
    msg_matrices.forEach(matrix => {
        let temp = [];
        temp.push([((k_inverse[0][0] * matrix[0]) + (k_inverse[1][0] * matrix[1])) % 26, ((k_inverse[0][1] * matrix[0] + k_inverse[1][1] * matrix[1])) % 26]);
        temp.forEach(t => {
            //console.log("LETTERS: ", t[0], t[1]);
            decrypted_text = decrypted_text + int_to_letter(t[0]);
            decrypted_text = decrypted_text + int_to_letter(t[1]);
        });
    });

    return decrypted_text;
}