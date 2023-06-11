import random
import os
import cv2
import matplotlib.pyplot as plt
import image_test
import sav

POLYGON_SIZE = 3
NUM_OF_POLYGONS = 110

# calculate total number of params in chromosome:
# For each polygon we have:
# two coordinates per vertex, 3 color values, one alpha value
NUM_OF_PARAMS = NUM_OF_POLYGONS * (POLYGON_SIZE * 2 + 4)

# set the random seed:
RANDOM_SEED = 1234
random.seed(RANDOM_SEED)

# create the image test class instance:
imageTest = image_test.ImageTest("Mona_Lisa_head.png", POLYGON_SIZE)

# calculate total number of params in chromosome:
# For each polygon we have:
# two coordinates per vertex, 3 color values, one alpha value
NUM_OF_PARAMS = NUM_OF_POLYGONS * (POLYGON_SIZE * 2 + 4)

# all parameter values are bound between 0 and 1, later to be expanded:
BOUNDS_LOW, BOUNDS_HIGH = 0.0, 1.0  # boundaries for all dimensions

# helper function for creating random real numbers uniformly distributed within a given range [low, up]
# it assumes that the range is the same for every dimension
def randomFloat(low, up):
    return [random.uniform(l, u) for l, u in zip([low] * NUM_OF_PARAMS, [up] * NUM_OF_PARAMS)]

# fitness calculation using MSE as difference metric:
def getDiff(individual):
    return imageTest.getDifference(individual, "MSE"),
    #return imageTest.getDifference(individual, "SSIM"),

# this function take polygons and save them into an image
def saveImage(gen, polygonData):
    # only every 100 generations:
    if gen % 100 == 0:
        # create folder if does not exist:
        folder = "images/results/run-{}-{}".format(POLYGON_SIZE, NUM_OF_POLYGONS)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # save the image in the folder:
        imageTest.saveImage(polygonData,
                            "{}/after-{}-gen.png".format(folder, gen),
                            "After {} Generations".format(gen))

# pertubation
def perturbation(elem):
    temp = []
    for i in elem:
      offset=i+random.uniform(-0.1, 0.1)
      casuale=random.randint(1, 128)
      if casuale==1:
        if offset<0:
          offset=0
        if offset>1:
          offset=1
        temp.append(offset)
      else: temp.append(i)
    perturbed = tuple(temp)
    return perturbed

# ils algorithm
def ils(n_iterations):
  # generate a random initial point for the search
  start_pt=randomFloat(BOUNDS_LOW,BOUNDS_HIGH)
  solution=start_pt
  solution_eval=getDiff(start_pt)[0]

  for i in range(n_iterations):
    # perform perturbation
    candidate=perturbation(solution)
  
    # evaluetion for candidate
    candidate_eval=getDiff(candidate)[0]

    # create and save an image every 1000 step
    if i%1000==0:
      print("sol ",i," --> ",solution_eval)
      print("cand ",i," --> ",candidate_eval)
      saveImage(i,solution)

    # if candidate is less then the current solution perform the substitution
    if candidate_eval <= solution_eval:
      # store the new point
      solution, solution_eval = candidate, candidate_eval

  # return the solution    
  return solution

# define the total iterations
n_iter = 200000

# run ils
best = ils(n_iter)
print(best)

#plot best solution
imageTest.plotImages(imageTest.polygonDataToImage(best))
plt.show()

#Per sfocare:
#origImage = cv2.imread('2-12-after-199000-ite-ssim.png')
#blurredImage = cv2.GaussianBlur(origImage, (45, 45), cv2.BORDER_DEFAULT)
#cv2.imwrite('blurred_ssim.png', blurredImage)