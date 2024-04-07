var emotion_label = document.querySelector('#Tree-hole-AI-response-emotion');
var emotion_response_text_label = document.querySelector('#Tree-hole-AI-response-text');
var emotion_saying_text_label = document.querySelector('#Tree-hole-AI-famous-saying');
let emotion_faces_label = $('#emotion-faces');

var emotion_analysis_result = 'Sad';
var emotion_classes = [
    'Neutral',
    'Happy',
    'Angry',
    'Fear',
    'Sad'
];

let sad_html =
    '<svg class="sad" width="44px" height="44px" viewBox="0 0 44 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
    '    <g id="sad" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(0, 0)">' +
    '        <circle id="body" fill="#E23D18" cx="22" cy="22" r="22"></circle>\n' +
    '        <g id="face" transform="translate(13.000000, 20.000000)">\n' +
    '            <g class="face">\n' +
    '            <path d="M7,4 C7,5.1045695 7.8954305,6 9,6 C10.1045695,6 11,5.1045695 11,4" class="mouth" stroke="#2C0E0F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" transform="translate(9.000000, 5.000000) rotate(-180.000000) translate(-9.000000, -5.000000) "></path>' +
    '            <ellipse class="right-eye" fill="#2C0E0F" cx="16.0941176" cy="1.75609756" rx="1.90588235" ry="1.75609756"></ellipse>' +
    '            <ellipse class="left-eye" fill="#2C0E0F" cx="1.90588235" cy="1.75609756" rx="1.90588235" ry="1.75609756"></ellipse>' +
    '          </g>' +
    '        </g>' +
    '    </g>' +
    '</svg>'

let neutral_html =
    '<svg class="neutral" width="44px" height="44px" viewBox="0 0 44 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
    '    <g>' +
    '        <circle id="body" fill="#F9AC1B" cx="22" cy="22" r="22"></circle>' +
    '        <g class="face">' +
    '          <g transform="translate(13.000000, 20.000000)" fill="#2C0E0F">' +
    '            <g class="mouth">' +
    '                <g transform="translate(9, 5)" >' +
    '                  <rect x="-2" y="0" width="4" height="2" rx="2"></rect>' +
    '                </g>' +
    '              </g>' +
    '              <ellipse class="right-eye" cx="16.0941176" cy="1.75" rx="1.90588235" ry="1.75"></ellipse>' +
    '              <ellipse class="left-eye" cx="1.90588235" cy="1.75" rx="1.90588235" ry="1.75"></ellipse>' +
    '          </g>' +
    '        </g>' +
    '    </g>' +
    '</svg>'

let fine_html =
    '<svg class="fine" width="44px" height="44px" viewBox="0 0 44 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
    '    <g id="fine-emotion" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">' +
    '        <g id="fine">' +
    '            <circle id="body" fill="#1988E3" cx="22" cy="22" r="22"></circle>' +
    '            <g class="matrix" transform="translate(22.000000, 32.000000)">' +
    '             <g class="face-container">' +
    '              <g class="face" transform="translate(-9, -12)">' +
    '                <g class="face-upAndDown">' +
    '                <g class="eyes">' +
    '                <ellipse class="right-eye" fill="#2C0E0F" cx="16.0941176" cy="1.75609756" rx="1.90588235" ry="1.75609756"></ellipse>' +
    '                <ellipse class="left-eye" fill="#2C0E0F" cx="1.90588235" cy="1.75609756" rx="1.90588235" ry="1.75609756"></ellipse></g>' +
    '                <path d="M6.18823529,4.90499997 C6.18823529,5.95249999 7.48721095,7 9.08957864,7 C10.6919463,7 11.990922,5.95249999 11.990922,4.90499997" id="mouth" stroke="#2C0E0F" stroke-linecap="round" stroke-linejoin="round"></path>' +
    '                </g>' +
    '            </g>' +
    '            </g>' +
    '          </g>' +
    '        </g>' +
    '    </g>' +
    '</svg>'

let happy_html =
    '<svg class="happy" width="44px" height="44px" viewBox="0 0 44 44" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
    '      <g id="Happy" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(0, 0)">' +
    '          <circle id="Body" fill="#248C37" cx="22" cy="22" r="22"></circle>' +
    '        <g class="scaleFace">' +
    '          <g class="face">  ' +
    '            <ellipse id="Eye-right" fill="#2C0E0F" cx="29.0875" cy="21.75" rx="1.89926471" ry="1.75"></ellipse>' +
    '              <ellipse id="Eye-left" fill="#2C0E0F" cx="14.8992647" cy="21.75" rx="1.89926471" ry="1.75"></ellipse>' +
    '              <path d="M21.8941176,27.8819633 C24.8588235,27.8819632 25.4941176,25.5404999 25.4941176,24.5648901 C25.4941176,23.5892803 24.4352941,23.9795242 22.1058824,23.9795242 C19.7764706,23.9795242 18.2941176,23.5892803 18.2941176,24.5648901 C18.2941176,25.5404999 18.9294118,27.8819633 21.8941176,27.8819633 Z" id="Mouth" fill="#2C0E0F"></path>' +
    '              <ellipse id="Tung" fill="#E23D18" cx="21.8941176" cy="26.4390244" rx="1.69411765" ry="0.780487805"></ellipse>' +
    '          </g>  ' +
    '      </g>' +
    '  </svg>'

if (emotion_analysis_result == 'Neutral'){
    emotion_faces_label.append(neutral_html);
    emotion_label.textContent = 'Peaceful and stable mood';
    emotion_response_text_label.textContent = 'Neutral emotions can be likened to a tranquil oasis amidst life\'s storms, offering a respite from intense highs and lows. In this state, one can find clarity and objectivity, facilitating rational thinking and thoughtful consideration of situations. It\'s a state of equilibrium where one can observe without being swayed by strong emotions, fostering a sense of inner peace and stability.';
    emotion_saying_text_label = '"True happiness is to enjoy the present, without anxious dependence upon the future, not to amuse ourselves with either hopes or fears but to rest satisfied with what we have, which is sufficient, for he that is so wants nothing. The greatest blessings of mankind are within us and within our reach. A wise man is content with his lot, whatever it may be, without wishing for what he has not." -- Stoic philosopher Seneca ';

}else if (emotion_analysis_result == 'Happy'){
    emotion_faces_label.append(happy_html);
    emotion_label.textContent = 'Happy and light mood';
    emotion_response_text_label.textContent = 'The Happy emotion is a beautiful and uplifting experience that brightens our days and fills our hearts with joy. It allows us to appreciate the beauty of life, cherish moments of connection with others, and find contentment in the simplest of pleasures. Happiness fosters resilience, strengthens relationships, and enhances overall well-being. It\'s a beacon of positivity that radiates warmth and optimism, inspiring us to embrace each day with gratitude and enthusiasm.';
    emotion_saying_text_label.textContent = '"Happiness is a butterfly, which when pursued, is always just beyond your grasp, but if you sit down quietly, may alight upon you." - Nathaniel Hawthorne';

}else if (emotion_analysis_result == 'Angry'){
    emotion_faces_label.append(fine_html);
    emotion_label.textContent = 'Rushing and unstable mood';
    emotion_response_text_label.textContent = 'One positive aspect of the emotion of anger is that it can serve as a powerful motivator for change. When channeled constructively, anger can fuel determination and action in addressing injustices, setting boundaries, or rectifying situations that are unsatisfactory. It can drive individuals to stand up for themselves or for others, leading to positive outcomes such as social progress, personal growth, and the establishment of healthier relationships. Anger, when managed effectively, can thus become a catalyst for positive transformation and empowerment.';
    emotion_saying_text_label.textContent = '"Every day we have plenty of opportunities to get angry, stressed or offended. But what you\'re doing when you indulge these negative emotions is giving something outside yourself power over your happiness. You can choose to not let little things upset you." - Joel Osteen';

}else if (emotion_analysis_result == 'Sad'){
    emotion_faces_label.append(sad_html);
    emotion_label.textContent = 'Blue and sorrowful mood';
    emotion_response_text_label.textContent = 'Emotions like sadness can prompt introspection and self-awareness, leading to personal growth and resilience. Additionally, experiencing sadness allows for a deeper appreciation of the contrasting moments of joy and contentment in life, enhancing emotional richness and understanding. It can also foster empathy and compassion towards others who may be going through similar emotions, strengthening connections and relationships. Ultimately, embracing and navigating through feelings of sadness can contribute to a more balanced and fulfilling emotional life.';
    emotion_saying_text_label.textContent = '"Out of suffering have emerged the strongest souls; the most massive characters are seared with scars." - Khalil Gibran';

}else if (emotion_analysis_result == 'Fear'){
    emotion_faces_label.append(fine_html);
    emotion_label.textContent = 'Uncertain and fear mood';
    emotion_response_text_label.textContent = 'When we experience fear, it often signals that we are stepping outside of our comfort zone or facing a challenge. Embracing fear can lead us to confront obstacles, develop resilience, and ultimately achieve personal and professional growth. Additionally, fear can sharpen our focus, heighten our senses, and propel us to take necessary precautions, helping to keep us safe and prepared in various situations. In this way, fear can be a catalyst for empowerment and self-improvement.';
    emotion_saying_text_label.textContent = '"Expose yourself to your deepest fear; after that, fear has no power, and the fear of freedom shrinks and vanishes. You are free." - Jim Morrison';
}
