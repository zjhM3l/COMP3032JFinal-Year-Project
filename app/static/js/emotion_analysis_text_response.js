var emotion_label = document.querySelector('#Tree-hole-AI-response-emotion');
var emotion_response_text_label = document.querySelector('#Tree-hole-AI-response-text');
var emotion_saying_text_label = document.querySelector('#Tree-hole-AI-famous-saying');

var emotion_analysis_result = 'Neutral';
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

}else if (emotion_analysis_result == 'Angry'){
    emotion_label.textContent = 'Rushing and unstable mood';

}else if (emotion_analysis_result == 'Sad'){
    emotion_label.textContent = 'Blue and sorrowful mood';

}else if (emotion_analysis_result == 'Fear'){
    emotion_label.textContent = 'Uncertain and fear mood';
}
