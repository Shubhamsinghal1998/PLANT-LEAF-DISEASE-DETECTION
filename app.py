import streamlit as st
#for defining the loss in compile function
import tensorflow as tf

#for loading the model trained earlier for prediction purpose
from tensorflow.keras.models import load_model

#for loading the image and making changes in it
#to make it fit for prediction purpose
from tensorflow.keras import preprocessing

import numpy as np
st.set_page_config(page_title="Leaf Disease Detection", layout="wide")

# Define the solutions for each category
solutionsPotato = {
    "Potato Healthy": """
    **Action:** Maintain regular crop monitoring and good agricultural practices.\n
    **Preventive Measures:** Ensure proper irrigation, use balanced fertilizers, and control pests.\n
    **Soil Health:** Rotate crops to maintain soil fertility and prevent disease build-up.\n
    **Surveillance:** Continue regular inspections to catch any early signs of disease or pests.\n
    """,
    "Potato Early Blight": """
    **Immediate Action:** Remove and destroy infected leaves to prevent the spread.\n
    **Fungicide Application:** Apply fungicides like chlorothalonil or mancozeb at the first sign of disease.\n
    **Crop Rotation:** Avoid planting potatoes or related crops in the same soil for at least two years.\n
    **Healthy Practices:** Ensure adequate spacing and airflow between plants to reduce humidity and fungal growth.\n
    """,
    "Potato Late Blight": """
    **Immediate Action:** Remove and destroy all infected plants and plant debris.\n
    **Fungicide Treatment:** Use fungicides such as metalaxyl or copper-based sprays regularly during humid conditions.\n
    **Resistant Varieties:** Plant potato varieties that are resistant to late blight.\n
    **Water Management:** Avoid overhead irrigation and ensure proper drainage to reduce leaf wetness duration.\n
    """
}

solutionsTomato = {
    "Tomato - Bacteria Spot Disease": """
    **Immediate Action:** Remove and destroy affected leaves to reduce spread.\n
    **Copper Sprays:** Apply copper-based bactericides weekly to manage the disease.\n
    **Preventive Measures:** Avoid overhead watering to reduce leaf wetness.\n
    **Sanitation:** Disinfect gardening tools and avoid working with wet plants.
    """,
    "Tomato - Early Blight Disease": """
    **Immediate Action:** Remove and destroy infected plant parts.\n
    **Fungicide Application:** Apply fungicides like chlorothalonil or copper-based sprays at the first sign of disease.\n
    **Crop Rotation:** Rotate crops and avoid planting tomatoes in the same soil for at least two years.\n
    **Healthy Practices:** Ensure proper spacing and air circulation around plants.
    """,
    "Tomato - Healthy and Fresh": """
    **Action:** Maintain regular crop monitoring and good agricultural practices.\n
    **Preventive Measures:** Ensure proper irrigation, use balanced fertilizers, and control pests.\n
    **Soil Health:** Rotate crops to maintain soil fertility and prevent disease build-up.\n
    **Surveillance:** Continue regular inspections to catch any early signs of disease or pests.
    """,
    "Tomato - Late Blight Disease": """
    **Immediate Action:** Remove and destroy all infected plants and plant debris.\n
    **Fungicide Treatment:** Use fungicides such as metalaxyl or copper-based sprays regularly during humid conditions.\n
    **Resistant Varieties:** Plant tomato varieties that are resistant to late blight.\n
    **Water Management:** Avoid overhead irrigation and ensure proper drainage to reduce leaf wetness duration.
    """,
    "Tomato - Leaf Mold Disease": """
    **Immediate Action:** Remove and destroy affected leaves to reduce inoculum.\n
    **Ventilation:** Improve air circulation by pruning and spacing plants appropriately.\n
    **Fungicide Application:** Use fungicides like chlorothalonil or copper-based sprays as preventive measures.\n
    **Humidity Control:** Reduce humidity in greenhouses by venting and reducing plant density.
    """,
    "Tomato - Septoria Leaf Spot Disease": """
    **Immediate Action:** Remove and destroy infected leaves to prevent spread.\n
    **Fungicide Application:** Apply fungicides like chlorothalonil or mancozeb at the first sign of disease.\n
    **Watering Practices:** Water at the base of plants to avoid wetting the foliage.\n
    **Sanitation:** Rotate crops and avoid planting tomatoes in the same soil for at least two years.
    """,
    "Tomato - Target Spot Disease": """
    **Immediate Action:** Remove and destroy affected plant parts.\n
    **Fungicide Treatment:** Use fungicides like azoxystrobin or copper-based sprays regularly.\n
    **Crop Rotation:** Rotate crops to prevent the build-up of soil-borne pathogens.\n
    **Healthy Practices:** Maintain good air circulation and avoid overhead irrigation.
    """,
    "Tomato - Tomato Yellow Leaf Curl Virus Disease": """
    **Immediate Action:** Remove and destroy infected plants immediately to prevent spread.\n
    **Insect Control:** Use insecticides or biological controls to manage whitefly populations, which spread the virus.\n
    **Resistant Varieties:** Plant tomato varieties that are resistant to TYLCV.\n
    **Preventive Measures:** Use reflective mulches to repel whiteflies and install physical barriers.
    """,
    "Tomato - Tomato Mosaic Virus Disease":"""
    **Immediate Action:** Wash off mites with a strong stream of water.\n
    **Biological Control:** Introduce natural predators like ladybugs or predatory mites.\n
    **Miticide Application:** Use miticides if the infestation is severe and other methods are not effective.\n
    **Healthy Practices:** Maintain proper watering and avoid plant stress to reduce susceptibility to mosaic virus.
    """,
    "Tomato - Two Spotted Spider Mite Disease": """
    **Immediate Action:** Wash off mites with a strong stream of water.\n
    **Biological Control:** Introduce natural predators like ladybugs or predatory mites.\n
    **Miticide Application:** Use miticides if the infestation is severe and other methods are not effective.\n
    **Healthy Practices:** Maintain proper watering and avoid plant stress to reduce susceptibility to mites.
    """
}

solutionsCotton= {
"Aphids":'''
**Prevention:**
- **Introduce beneficial insects:** Ladybugs and lacewings are natural predators of aphids.
- **Plant companion plants:** Plants like garlic, chives, and marigolds can repel aphids.
- **Regular monitoring:** Inspect plants regularly to catch infestations early.

**Cure:**
- **Insecticidal soap:** Use insecticidal soap sprays to kill aphids on contact.
- **Neem oil:** Neem oil is effective against aphids and other soft-bodied insects.
- **Water spray:** A strong spray of water can dislodge aphids from plants.
''',
"Army Worm":'''
**Prevention:**
- **Crop rotation:** Rotate crops to disrupt the life cycle of army worms.
- **Early planting:** Plant crops early in the season to avoid peak army worm activity.
- **Remove debris:** Keep the garden clean by removing plant debris where army worms can hide.

**Cure:**
- **Bacillus thuringiensis (Bt):** A natural bacterium that is toxic to caterpillars.
- **Spinosad:** A natural insecticide derived from a soil bacterium.
- **Handpicking:** Manually remove army worms from plants.
''',
"Bacterial Blight":'''
**Prevention:**
- **Use resistant varieties:** Plant disease-resistant varieties when available.
- **Sanitize tools:** Regularly disinfect gardening tools to prevent the spread of bacteria.
- **Proper spacing:** Ensure proper spacing between plants to promote air circulation.

**Cure:**
- **Copper-based bactericides:** Can help control the spread of bacterial blight.
- **Remove infected plants:** Promptly remove and destroy infected plants to prevent the spread.
- **Avoid overhead watering:** Use drip irrigation to minimize leaf wetness.
''',
"Healthy Leaf":'''
(No action needed for healthy leaves as this indicates no disease presence.)
''',
"Powdery Mildew":'''
**Prevention:**
- **Choose resistant varieties:** Select plant varieties that are resistant to powdery mildew.
- **Adequate spacing:** Ensure plants are spaced properly to allow good air circulation.
- **Avoid over-fertilization:** Excessive nitrogen can promote powdery mildew growth.

**Cure:**
- **Neem oil:** Effective in controlling powdery mildew.
- **Baking soda spray:** A mixture of baking soda, water, and a few drops of dish soap can be used.
- **Sulfur sprays:** Can prevent the spread if applied early.
''',
"Target Spot":'''
**Prevention:**
- **Crop rotation:** Rotate crops to prevent the buildup of pathogens in the soil.
- **Remove plant debris:** Clear plant debris to eliminate potential breeding grounds.
- **Proper irrigation:** Water plants at the base to avoid wetting the foliage.

**Cure:**
- **Fungicides:** Use fungicides containing chlorothalonil or mancozeb.
- **Remove affected leaves:** Remove and destroy affected leaves to reduce the spread.
- **Improve air circulation:** Prune plants to enhance airflow and reduce humidity.
'''
}

solutionsPepper= {
    "Pepper bell Bacterial Spot":'''
## Pepper Bell Bacterial Spot

### Preventions
1. **Crop Rotation**: Rotate crops to prevent the buildup of bacterial pathogens in the soil. Avoid planting peppers in the same location more than once every three years.
2. **Use Disease-Free Seeds**: Purchase seeds from reputable sources and use certified disease-free transplants.
3. **Sanitation**: Remove and destroy infected plant debris and weeds that may harbor the bacteria.
4. **Water Management**: Avoid overhead irrigation to reduce leaf wetness. Use drip irrigation instead to keep foliage dry.
5. **Mulching**: Apply mulch to reduce soil splashing onto leaves, which can spread bacteria.
6. **Resistant Varieties**: Plant pepper varieties that are resistant to bacterial spot if available.
7. **Proper Spacing**: Ensure adequate spacing between plants to improve air circulation and reduce humidity.

### Cures
1. **Copper-Based Sprays**: Apply copper-based bactericides regularly, starting when symptoms first appear. Follow label instructions for application rates and timings.
2. **Antibiotics**: In some cases, streptomycin or other antibiotics may be recommended, but use them judiciously to avoid resistance.
3. **Remove Infected Plants**: Uproot and destroy severely infected plants to prevent the spread of bacteria.
4. **Prune Affected Areas**: Remove infected leaves and stems carefully to reduce bacterial load.
''',
"Pepper bell healthy":'''
## Pepper Bell Healthy

### Maintenance Tips
1. **Regular Monitoring**: Check plants frequently for signs of pests or disease to catch problems early.
2. **Proper Nutrition**: Provide balanced fertilization to ensure healthy plant growth. Avoid over-fertilizing with nitrogen, which can make plants more susceptible to diseases.
3. **Watering Practices**: Water plants at the base and keep foliage dry to prevent fungal and bacterial infections.
4. **Weed Control**: Keep the area around pepper plants free of weeds, which can harbor pests and diseases.
5. **Good Air Circulation**: Space plants adequately and prune as necessary to ensure good air circulation around the plants.
6. **Soil Health**: Maintain healthy soil with organic matter and proper pH levels. Conduct soil tests to monitor nutrient levels and adjust as needed.
'''
}


def identify_pepper_plant_disease(uploaded_file):
    # target dimensions of image
    img_width, img_height = 256, 256

    # load the model we saved
    model = load_model('vit_bell_pepper.h5')

    # predicting on new data
    #creating an object of image and changing its size to required size
    img = preprocessing.image.load_img(uploaded_file, target_size=(img_width, img_height))
    
    #converting the image to array
    img_array = preprocessing.image.img_to_array(img)
    # img_array = tf.expand_dims(img_array, 0) # create a batch
    img_array = np.expand_dims(img_array, axis=0)
    image = np.vstack([img_array])

    #gives probability for each class
    prob = model.predict(image)

    #possible classes
    class_= ['Pepper bell Bacterial Spot','Pepper bell healthy']

    st.write(f"Identified Disease is {class_[np.argmax(prob)]}.")

    return solutionsPepper[class_[np.argmax(prob)]]

def identify_cotton_plant_disease(uploaded_file):
    # target dimensions of image
    img_width, img_height = 180, 180

    # load the model we saved
    model = load_model('cottonModel.h5')

    # predicting on new data
    #creating an object of image and changing its size to required size
    img = preprocessing.image.load_img(uploaded_file, target_size=(img_width, img_height))
    
    #converting the image to array
    img_array = preprocessing.image.img_to_array(img)
    # img_array = tf.expand_dims(img_array, 0) # create a batch
    img_array = np.expand_dims(img_array, axis=0)
    image = np.vstack([img_array])

    #gives probability for each class
    prob = model.predict(image)

    #possible classes
    class_= ['Aphids','Army Worm','Bacterial Blight','Healthy Leaf','Powdery Mildew','Target Spot']

    st.write(f"Identified Disease is {class_[np.argmax(prob)]}.")

    return solutionsCotton[class_[np.argmax(prob)]]


def identify_potato_disease(uploaded_file):
    # target dimensions of image
    img_width, img_height = 256, 256

    # load the model we saved
    model = load_model('potatoModel.h5')

    # predicting images
    #creating an object of image and changing its size to required size
    img = preprocessing.image.load_img(uploaded_file, target_size=(img_width, img_height))

    #converting the image to array
    x = preprocessing.image.img_to_array(img)

    x = np.expand_dims(x, axis=0)
    image = np.vstack([x])
    
    #gives probability for each class
    prob = model.predict(image)

    #possible classes
    class_= ['Potato Early Blight', 'Potato Late Blight', 'Potato Healthy']

    st.write(f"Identified Disease is {class_[np.argmax(prob)]}.")

    return solutionsPotato[class_[np.argmax(prob)]]

def identify_tomato_disease(uploaded_file):

    # target dimensions of image
    img_width, img_height = 128, 128

    # load the model we saved
    model = load_model('tomatoModel.h5')

    # predicting images
    #creating an object of image and changing its size to required size
    img = preprocessing.image.load_img(uploaded_file, target_size=(img_width, img_height))

    #converting the image to array
    x = preprocessing.image.img_to_array(img)

    x = np.expand_dims(x, axis=0)
    image = np.vstack([x])
    
    #gives probability for each class
    prob = model.predict(image)

    #possible classes
    class_= ['Tomato - Bacteria Spot Disease', 'Tomato - Early Blight Disease', 'Tomato - Healthy and Fresh',
             'Tomato - Late Blight Disease','Tomato - Leaf Mold Disease','Tomato - Septoria Leaf Spot Disease',
             'Tomato - Target Spot Disease','Tomato - Tomoato Yellow Leaf Curl Virus Disease','Tomato - Tomato Mosaic Virus Disease',
             'Tomato - Two Spotted Spider Mite Disease']
    
    st.write(f"Identified Disease is {class_[np.argmax(prob)]}.")

    return solutionsTomato[class_[np.argmax(prob)]]

def identify_disease(uploaded_file, plant_type):
    # Placeholder function for disease identification
    # Replace with actual model prediction code

    disease= ''
    if plant_type=="Potato":
        disease= identify_potato_disease(uploaded_file)
    elif plant_type=='Tomato':
        disease= identify_tomato_disease(uploaded_file)
    elif plant_type=='Cotton':
        disease= identify_cotton_plant_disease(uploaded_file)
    else:
        disease= identify_pepper_plant_disease(uploaded_file)

    return disease


original_title = '<h1 style="font-family: serif; color: ;font-size:40px;"><u>PLANT LEAF DISEASE DETECTION USING DIGITAL IMAGE✨</u></h1>'
st.markdown(original_title, unsafe_allow_html=True)


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://getwallpapers.com/wallpaper/full/3/b/a/1190437-vertical-green-leaf-wallpaper-hd-2560x1600.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)
st.title("🌿 Leaf Guardian: Detect Plant Diseases in a Snap! 🌿")
st.write("")
st.write('''Welcome to Leaf Guardian, your go-to app for quick and accurate plant disease detection. 
Just upload a leaf photo, and let our AI-powered tool do the rest! 
Now supporting Potato, Tomato, Pepper and Cotton plants.''')

st.header("🌱 Upload Your Leaf Image")
st.write("Upload a clear image of a potato, tomato, or cotton leaf to identify any disease.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Example image button
if st.button("Show Example Image"):
    st.image("example_leaf.jpg", caption="Example Leaf Image")
    

st.header("🍅 Select Plant Type 🥔")
plant_type = st.radio("Choose the plant type:", 
                      [("Potato", "🥔 Potato"),
                       ("Tomato", "🍅 Tomato"), 
                       ("Cotton", "🌾 Cotton"),
                       ("Pepper", "🌶️ Pepper")],
                      format_func=lambda x: x[1])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Leaf Image')
    st.write("")
    if st.button('🔍 Identify Disease'):
        with st.spinner('Identifying disease...'):
            # Placeholder for the model prediction function
            disease = identify_disease(uploaded_file, plant_type[0])
            st.success(f'{disease}')

st.header("Tips for Taking Good Leaf Images")
st.write("""
- Ensure the leaf is clean and free from water droplets.
- Take the picture in good lighting conditions.
- Avoid shadows on the leaf.
- Ensure the leaf is in focus and occupies most of the image frame.
""")
st.header("Contact Us For Any Query")
st.write("""
- Contact us for personalised help, where one can ask their queries and can conclude through the FAQs.
- Advising on best practices to guide farmers so that they can use advance techniques.
- EMAIL:-singhalshubham553@gmail.com shivamsharma8130949978@gmail.com
- MOB.NO:-9540131264 8130949978
""")
