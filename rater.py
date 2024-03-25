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
                 "surgery", "survival", "diagnosi(s|ng)", "MRI", "CT",
                 "whole slide", "X-ray", "cancer", "disease", "skin lesions",
                 "sign language", "clinical", "facial", "face", "cardiac",
                 "tumor", "endoscopic"],
                ["5G", "6G", "industrial", "IoT", "recommendation"],
                ["remote sensing", "UAV", "forecast(ing)?", "satellite"],
                ["edge (environments?|embedded systems?|computing|applications?)",
                 "edge[ -]cloud"],
                ["HDR", "image restoration", "haze", "dehazing"],
                ["quantum"],
            ],
            -1: [
                ["3D", "Gaussian splatting", "voxel", "point cloud", "6-?DoF",
                 "RGB-?D", "NeRF", "radiance fields", "avatar"],
                ["generative", "generation", "diffusion", "GAN",
                 "synthesi(s|ze|zer|zing)", "(image|video) edit(ing)?",
                 "text[ -]to[ -](image|video|vision)", "super[ -]?resolution"],
                ["(autonomous|automated) driving", "trajectory", "LiDAR"],
                ["robotics", "robot", "navigation"],
                ["federated learning"],
                ["reinforcement"],
                ["knowledge Edit(ing)?", "unlearning"],
                ["architecture search", "NAS"],
                ["GNNs?", "graph"],
                ["explainable", "interpretable"],
                ["attacks?"],
            ],
            1: [
                [r"\S*[ -]?efficient", "efficiency", "PEFT"],
                ["vision[ -]language"],
                ["bias"]
            ],
            0.5: [
                ["AAAI", "CVPR", "ECCV", "EMNLP", "ICASSP", "ICCV", "ICLR",
                 "Interspeech", "NeurIPS", "NIPS", "WACV"]
            ]
        }
    
    
    def subject(self, info):
        keywords = []
        finalRating = 0
        strInfo = " ".join(str(info).split())
        
        for rating in sorted(self.SubjectOfInterest.keys()):
            for keyword in self.SubjectOfInterest[rating]:
                if keyword in strInfo:
                    finalRating = rating
                    keywords.append(keyword)
        
        if (len(keywords) > 0): keywords = [keywords]
        
        return finalRating, keywords
    

    def phrase(self, info):
        keywords = []
        finalRating = 0
        strInfo = " ".join(str(info).split())

        for (rating, phrasesGroup) in sorted(self.PhraseOfInterest.items(), reverse = True):
            for phrases in phrasesGroup:
                matches = []

                for phrase in phrases:
                    phrase = r"\b" + phrase + r"\b"
                    m = re.search(phrase, strInfo, flags = re.IGNORECASE)
                    if (m != None): matches.append(m.group(0))

                if (len(matches) > 0):
                    finalRating += rating
                    keywords.append(matches)
        
        return finalRating, keywords


    def __call__(self, info):
        sbjRating, sbjKeywords = self.subject(info)
        phrRating, phrKeywords = self.phrase(info)

        keywords = sbjKeywords + phrKeywords
        rating = sbjRating + phrRating + (-0.5 if (len(keywords) == 0) else 0)
        
        return rating, keywords

rater = Rater()

if (__name__ == "__main__"):
    info = \
"""
"""
    print(rater(info))
