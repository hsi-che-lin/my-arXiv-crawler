from bs4 import BeautifulSoup
import re

class Rater:
    def __init__(self):
        """
        the rating of subject will only be count once i.e., paper with multiple
        matched subject will only get the rating of the highest rated subject
        """
        self.SubjectOfInterest = {
            1: [
                "cs.CV",    # Computer Vision and Pattern Recognition
                "eess.IV",  # Image and Video Processing
                "cs.CL",    # Computation and Language
                "cs.SD",    # Sound 
                "eess.AS",  # Audio and Speech Processing
            ],
            0.5: [
                "cs.AI",    # Artificial Intelligence
                "cs.LG",    # Machine Learning
                "cs.SI",    # Social and Information Networks
                "cs.CY"     # Computers and Society
            ]
        }

        """
        the rating of phrase will be count accumulatively i.e., paper will get
        sum of all rating of matched phrases (set)
        """
        self.PhraseOfInterest = {
            -2: [
                [r"bio\S*", "medical", "health", "healthcare", "surgical",
                 "surgery", "survival", "diagnosi(s|ng)", "f?MRI", "CT", "eeg",
                 "whole[- ]slide", "X-ray", "cancer", "disease", "skin lesions",
                 "sign language", "clinical", "facial", "cardiac", "tumor",
                 "endoscopic", "psychological", "pathological", "retinal?",
                 "red blood cells", "organ", "DNA", "radiology", "physiological",
                 "lesion"],
                ["5G", "6G", "industrial", "IoT", "recommendation", "patent",
                 "thermal", "alloys?", "chemistry", "chemical", "astronaut",
                 "astronomy", "watermark(ing)?", "FPGAs?"],
                ["remote(ly)? sens(ing|ed)", "UAV", "forecast(ing)?", "satellite",
                 "hyperspectral (data|imag(es?|ing))", "bird's-eye view", "BEV",
                 "drone", "agricultural", "mineral", "drill core", "seafloor"],
                ["HDR", "image restoration", "haze", "dehazing",
                 "neural( image)? codecs?", "quality assessment",
                 "((image|video|low-light)( quality| color)? enhancement)"],
                ["grammar", "grammatical", "named entity recognition"],
                ["song", "music", "text[ -]to[ -](music|audio|speech)",
                 "voice conversion"],
                ["quantum", "physics?"],
                ["tabulars?", "(my)?sql"],
                ["crimes?"]
            ],
            -1: [
                ["3D", "Gaussian splatting", "voxel", "point cloud", "(6|multi)-?DoFs?",
                 "6D", "RGB-?D", r"(?<!in(-| ))depth", "NeRF", "radiance fields",
                 "avatar", "event cameras?", "skeletons?", "signed distance fields?",
                 "SDF"],
                ["diffusion", "GAN", "inpaint(ing)?", "(image|video) edit(ing)?",
                 "text[ -]to[ -](image|video|vision)", "super[ -]?resolution",
                 "image retouching", "derain(ing)?"],
                ["(autonomous|automated) driving", "trajectory", "LiDAR", "radar",
                 "vehicle", "infrared", "flight", "SLAM", "re-identification"],
                ["speech enhancement"],
                ["robotics", "robot", "robotic manipulation", "navigation"],
                ["federated learning"],
                ["(knowledge|model) Edit(ing)?", "unlearning"],
                ["architecture search", "NAS"],
                ["GNNs?", "graphs?"],
                ["kernel learning", "SVM", "support vector machine"],
                ["anomaly detection", "deepfake"],
                ["attacks?"],
            ],
            1: [
                ["(parameters?|memory|time|training)[ -]?(efficient|efficiency)",
                 "PEFT", "efficient fine-?tun(e|ing)", "GPU memory"],
                ["(vision|visual)[ -]language", "VLMs?"],
                ["audio[ -](vision|visual)"],
                ["(social|cultral) bias(es)?"]
            ]
        }

        """
        the rating of conference will only be count once
        """
        self.ConferenceOfInterest = {
            0.5: [
                "AAAI", "CVPR", "ECCV", "EMNLP", "ICASSP", "ICCV", "ICLR",
                "Interspeech", "NeurIPS", "NIPS", "WACV", "ICML"
            ]
        }

    
    def matchOnce(self, ratingDict, content):
        keywords = []
        finalRating = 0
        
        for rating in sorted(ratingDict.keys()):
            for keyword in ratingDict[rating]:
                if (keyword in content):
                    keywords.append(keyword)
                    if (rating > finalRating):
                        finalRating = rating
        
        if (len(keywords) > 0): keywords = [keywords]
        
        return finalRating, keywords
    

    def matchAll(self, ratingDict, content):
        keywords = []
        finalRating = 0

        for (rating, phrasesGroup) in sorted(ratingDict.items(), reverse = True):
            for phrases in phrasesGroup:
                matches = []

                for phrase in phrases:
                    phrase = r"\b" + phrase + r"\b"
                    m = re.search(phrase, content, flags = re.IGNORECASE)
                    if (m != None): matches.append(m.group(0))

                if (len(matches) > 0):
                    finalRating += rating
                    keywords.append(matches)
        
        return finalRating, keywords


    def __call__(self, title, subjects, abstract, comment):
        cntRating, cntKeywords = self.matchAll(self.PhraseOfInterest, title + " " + abstract)
        sbjRating, sbjKeywords = self.matchOnce(self.SubjectOfInterest, subjects)

        if (comment != None):
            cmtRating, cmtKeywords = self.matchOnce(self.ConferenceOfInterest, comment)
        else:
            cmtRating, cmtKeywords = 0, []

        keywords = cntKeywords + sbjKeywords + cmtKeywords
        rating = (cntRating + sbjRating + cmtRating) if (len(keywords) != 0) else -10
        
        return rating, keywords

rater = Rater()
