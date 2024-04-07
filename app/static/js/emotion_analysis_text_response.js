var emotion_label = document.querySelector('#Tree-hole-AI-response-emotion');
var emotion_response_text_label = document.querySelector('#Tree-hole-AI-response-text');
var emotion_saying_text_label = document.querySelector('#Tree-hole-AI-famous-saying');

var emotion_analysis_result = 'Happy';
var emotion_classes = [
    'Neutral',
    'Happy',
    'Angry',
    'Fear',
    'Sad'
];

if (emotion_analysis_result == 'Neutral'){
    emotion_label.textContent = 'Peaceful and stable mood';
    emotion_response_text_label.textContent = 'Neutral emotions can be likened to a tranquil oasis amidst life\'s storms, offering a respite from intense highs and lows. In this state, one can find clarity and objectivity, facilitating rational thinking and thoughtful consideration of situations. It\'s a state of equilibrium where one can observe without being swayed by strong emotions, fostering a sense of inner peace and stability.';
    emotion_saying_text_label = '"True happiness is to enjoy the present, without anxious dependence upon the future, not to amuse ourselves with either hopes or fears but to rest satisfied with what we have, which is sufficient, for he that is so wants nothing. The greatest blessings of mankind are within us and within our reach. A wise man is content with his lot, whatever it may be, without wishing for what he has not." -- Stoic philosopher Seneca ';

}else if (emotion_analysis_result == 'Happy'){
    emotion_label.textContent = 'Happy and light mood';
    emotion_response_text_label.textContent = 'The Happy emotion is a beautiful and uplifting experience that brightens our days and fills our hearts with joy. It allows us to appreciate the beauty of life, cherish moments of connection with others, and find contentment in the simplest of pleasures. Happiness fosters resilience, strengthens relationships, and enhances overall well-being. It\'s a beacon of positivity that radiates warmth and optimism, inspiring us to embrace each day with gratitude and enthusiasm.';
    emotion_saying_text_label.textContent = '"Happiness is a butterfly, which when pursued, is always just beyond your grasp, but if you sit down quietly, may alight upon you." - Nathaniel Hawthorne';

}else if (emotion_analysis_result == 'Angry'){
    emotion_label.textContent = 'Rushing and unstable mood';
    emotion_response_text_label.textContent = 'One positive aspect of the emotion of anger is that it can serve as a powerful motivator for change. When channeled constructively, anger can fuel determination and action in addressing injustices, setting boundaries, or rectifying situations that are unsatisfactory. It can drive individuals to stand up for themselves or for others, leading to positive outcomes such as social progress, personal growth, and the establishment of healthier relationships. Anger, when managed effectively, can thus become a catalyst for positive transformation and empowerment.';
    emotion_saying_text_label.textContent = '"Every day we have plenty of opportunities to get angry, stressed or offended. But what you\'re doing when you indulge these negative emotions is giving something outside yourself power over your happiness. You can choose to not let little things upset you." - Joel Osteen';

}else if (emotion_analysis_result == 'Sad'){
    emotion_label.textContent = 'Blue and sorrowful mood';
    emotion_response_text_label.textContent = 'Emotions like sadness can prompt introspection and self-awareness, leading to personal growth and resilience. Additionally, experiencing sadness allows for a deeper appreciation of the contrasting moments of joy and contentment in life, enhancing emotional richness and understanding. It can also foster empathy and compassion towards others who may be going through similar emotions, strengthening connections and relationships. Ultimately, embracing and navigating through feelings of sadness can contribute to a more balanced and fulfilling emotional life.';
    emotion_saying_text_label.textContent = '"Out of suffering have emerged the strongest souls; the most massive characters are seared with scars." - Khalil Gibran';

}else if (emotion_analysis_result == 'Fear'){
    emotion_label.textContent = 'Uncertain and fear mood';
    emotion_response_text_label.textContent = 'When we experience fear, it often signals that we are stepping outside of our comfort zone or facing a challenge. Embracing fear can lead us to confront obstacles, develop resilience, and ultimately achieve personal and professional growth. Additionally, fear can sharpen our focus, heighten our senses, and propel us to take necessary precautions, helping to keep us safe and prepared in various situations. In this way, fear can be a catalyst for empowerment and self-improvement.';
    emotion_saying_text_label.textContent = '"Expose yourself to your deepest fear; after that, fear has no power, and the fear of freedom shrinks and vanishes. You are free." - Jim Morrison';
}
