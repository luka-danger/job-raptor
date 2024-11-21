export function truncateDescription(description, wordLimit) {
    const cleaned = description.replace(/\s+/g, ' ').trim();
    const words = cleaned.split(' ');

    if (words.length > wordLimit) {
        return words.slice(0, wordLimit).join(' ') + '...';
    }

    return cleaned
}