import { useState, useEffect } from 'react';
import { typeSentence, deleteSentence, animation, waitForMs } from './animation';

export const useAnimation = () => {
  const [typedText, setTypedText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    let isMounted = true;

    const animateText = async () => {
      const currentText = animation[currentIndex];

      if (!isMounted) return;
      await typeSentence(currentText, setTypedText);
      await waitForMs(2000);
      if (!isMounted) return;
      await deleteSentence(currentText, setTypedText);

      if (!isMounted) return;
      setCurrentIndex((prevIndex) => (prevIndex + 1) % animation.length);
    };

    animateText();

    return () => {
      isMounted = false;
    };
  }, [currentIndex]);

  return typedText; // Return the typed text for use in the component
};
