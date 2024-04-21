function findPosition(char, matrix) {

    // debug
    console.log("findPosition loaded");
    console.log("char: ", char);
    console.log("matrix: ", matrix);
    //

    for (let i = 0; i < matrix.length; i++) {
        let row = matrix[i];
        let index = row.indexOf(char);
        console.log("row: ", row);
        console.log("index: ", index);
        if (index !== -1) {
            return [i, index];
        }
    }
    return null;
}

function playfair_decryption(cipher, key) {
    const maxKeyLength = 25;

    // debug
    console.log("playfair_decryption loaded");
    //

    if (key.length > maxKeyLength) {
        console.log("Key must be 25 characters long or less.");
        return;
    }
    if (!/^[a-zA-Z]+$/.test(key)) {
        console.log("Key must not contain any numbers or symbols.");
        return;
    }
    if (!/^[a-zA-Z]+$/.test(cipher)) {
        console.log("Cipher must not contain any numbers or symbols.");
        return;
    }

    // Reformat cipher and key
    key = key.toUpperCase().replace(/ /g, "");
    cipher = cipher.toUpperCase().replace(/ /g, "");

    // Initializations for Playfair cipher
    // filter duplicates
    let seen = new Set();
    let processedKey = [];
    for (const char of key) {
        if (!seen.has(char)) {
            processedKey.push(char);
            seen.add(char);
        }
    }

    const alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    let remainingLetters = [...alphabet].filter(x => !seen.has(x));

    let finalChars = processedKey.concat(remainingLetters);

    // DEBUG
    console.log("processedkey: ", processedKey);
    console.log("remainingLetters: ", remainingLetters);
    console.log("finalchars:", finalChars);
    //

    let keyMatrix = Array.from({ length: 5 }, () => Array(5));
    let index = 0;
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            if (index < finalChars.length) {
                keyMatrix[i][j] = finalChars[index];
                index++;
            }
        }
    }

    // For debugging
    console.log(keyMatrix.map(row => row.join(' ')).join('\n'));
    //

    // Process the cipher text
    let appendedCharFlag = 0;
    if (cipher.length % 2 !== 0) {
        cipher += 'X';
        appendedCharFlag = 1;
    }

    let plainText = "";

    for (let i = 0; i < cipher.length; i += 2) {
        let char1 = cipher[i];
        let char2 = cipher[i + 1];

        let [row1, col1] = findPosition(char1, keyMatrix);
        let [row2, col2] = findPosition(char2, keyMatrix);

        if (row1 === row2) {
            // Same row: shift left
            col1 = (col1 - 1 + 5) % 5;
            col2 = (col2 - 1 + 5) % 5;
        } else if (col1 === col2) {
            // Same column: shift up
            row1 = (row1 - 1 + 5) % 5;
            row2 = (row2 - 1 + 5) % 5;
        } else {
            // Rectangle swap: swap columns
            [col1, col2] = [col2, col1];
        }

        plainText += keyMatrix[row1][col1] + keyMatrix[row2][col2];
    }

    // If odd number of characters in encrypted text, trim tail
    if (appendedCharFlag === 1) {
        plainText = plainText.slice(0, -1);
    }

    console.log(plainText);
    return plainText;
}