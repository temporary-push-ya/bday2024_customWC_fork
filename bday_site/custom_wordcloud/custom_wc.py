import matplotlib.pyplot as plt
from django.conf import settings
import numpy as np
from PIL import Image
import os
# np.random.seed(100)

wordcloud_debug = False

class wc_generator():
    mask_path = None
    def __init__(self, text, option):
        self.text = text
        if option == "heart":
            if wordcloud_debug:
                self.mask_path = "heart_mask_1.png"
                self.bcg_path = "heart_bcg.png"
            else:
                self.mask_path = os.path.join(settings.STATICFILES_DIRS[0], "images/heart_mask.png")
                self.bcg_path = os.path.join(settings.STATICFILES_DIRS[0], "images/heart_bcg.png")
         
        elif option == "star":
            self.mask_path = "star_mask.png"
            self.bcg_path = "star_bcg.png"
        elif option == "you":
            self.mask_path = "you_mask.png"
            self.bcg_path = "you_bcg.png"
        else:
            raise Exception("Invalid option")

    

    def generate(self):
        # (100,100,4) -> (100,100)
        heart_mask = np.array(Image.open(self.mask_path))[:,:,0]
        heart_mask = heart_mask[::-1] # array ind to plot ind
        heart_bcg = np.array(Image.open(self.bcg_path))[:,:,0]
        heart_bcg = heart_bcg[::-1] # array ind to plot ind

        np.savetxt("plt_mask.csv", heart_mask, delimiter=",", fmt = '%i') # debugging purposes

        # get pts
        pts = []
        x_bcg = []
        y_bcg = []
        x_min, x_max, y_min, y_max = np.inf, 0, np.inf, 0
        for y_i,y in enumerate(heart_mask):
            for x_i,x in enumerate(y):
                if heart_bcg[y_i][x_i] < 255:  # bcg
                    x_bcg.append(x_i)
                    y_bcg.append(y_i)
                if x == 0: # mask
                    pts.append((x_i,y_i))
                if x_i < x_min:
                    x_min = x_i
                if x_i > x_max:
                    x_max = x_i
                if y_i < y_min:
                    y_min = y_i
                if y_i > y_max:
                    y_max = y_i

        words = self.text.split()
        if len(words) > len(pts):
            words = words[:len(pts)]

        sample_ind = set(np.random.randint(0, len(pts), len(words)))

        # array pts -> (x,y) pts
        plot_pts = sorted(pts, key=lambda x: x[1]**3-x[0], reverse=True)

        inc = 0
        fig, ax = plt.subplots()
        for i, xy in enumerate(plot_pts):
            if i in sample_ind:
                ax.text(xy[0], xy[1], words[inc], fontsize=20, font='cambria', color='red',
                        horizontalalignment='center', verticalalignment='center')
                inc += 1

        # while creating the django site 
        if settings.DEBUG:
            print(f' there are totla: {len(pts)} black pts and {len(plot_pts)} points picked,\n words in sentence are {len(words)}')
            print(f'highest plot point:{np.max(y_bcg)} ')
            print(f'highest pts point:{np.max(list(map(lambda x:x[1], pts)))}')

        ax.scatter(x_bcg, y_bcg, c='darkred', marker='x', s=1)
        ax.set_xlim(x_min-10, x_max+10)
        ax.set_ylim(y_min-10, y_max+10)
        ax.axis("off")
        return fig

if __name__ == "__main__" and wordcloud_debug:
    text = "I can swallow a bottle of alcohol and I'll feel like Godzilla, Better hit the deck like the card dealer"
    wc = wc_generator(text, "heart")
    wc.generate()
    plt.show()