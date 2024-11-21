export const animation = [
    "Dig up the best positions with Job Raptor",
    "Raptor-approved jobs for your future",
    "Welcome to Job Raptor - Where opportunities roar!",
    "Job Raptor - a better way to job search"
]

export async function typeSentence(sentence, updateTextCallback, delay = 100) {
    const letters = sentence.split("");
    let typed = "";
    for (let i = 0; i < letters.length; i++) {
        await waitForMs(delay);
        typed += letters[i];
        updateTextCallback(typed);
    }
}

export async function deleteSentence(currentText, updateTextCallback, delay = 100) {
    if (typeof currentText !== 'string') {
      console.error("Invalid currentText passed to deleteSentence:", currentText);
      return; // Prevents errors if currentText is not a string
    }
  
    for (let i = currentText.length; i >= 0; i--) {
      await waitForMs(delay);
      updateTextCallback(currentText.slice(0, i));
    }
  }


export function waitForMs(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}