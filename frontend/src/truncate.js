export function truncateDescription(description, wordLimit) {
    if (description.includes('#URL_')) {
        return 'Description contains an invalid URL and cannot be displayed.';
    }

    const cleaned = description.replace(/\s+/g, ' ').trim();
    const words = cleaned.split(' ');

    if (words.length > wordLimit) {
        return words.slice(0, wordLimit).join(' ') + '...';
    }

    return cleaned
}