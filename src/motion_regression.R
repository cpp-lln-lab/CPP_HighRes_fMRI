library('ggplot2')
library('gridExtra')
library('tidyverse')

mocoPath <- '/Users/barilari/Desktop/data_temp/Marco_HighRes_new/derivatives/cpp_high-res_fmri/sub-pilot001/ses-008/func'

vasoFiles <- list.files(path = mocoPath, pattern = "vaso.txt$")

boldFiles <- list.files(path = mocoPath, pattern = "bold.txt$")

for (iRun in 1:length(vasoFiles)) {

outputName <-  paste('rp_sub-pilot001_ses-007_task-visualLocalizerFingerTapping_run-00', iRun, '.png', sep = '')

vasoFile <- vasoFiles[iRun]

boldFile <- boldFiles[iRun]

sourceVaso <- read.table(file = paste(mocoPath, vasoFile, sep = '/'), 
                         header = F)

sourceBold <- read.table(file = paste(mocoPath, boldFile, sep = '/'), 
                         header = F)

vaso <- sourceVaso %>% 
  set_names(c("x", "y", "z", "pitch", "roll", "yaw")) %>% 
  add_column(volume = 1:nrow(sourceVaso), sequence = "vaso") %>% 
  relocate("sequence", "volume","x", "y", "z", "pitch", "roll", "yaw")  %>% 
  pivot_longer(cols = c("x", "y", "z", "pitch", "roll", "yaw"),
               names_to = "motion_series", 
               values_to = "motion_param")

bold <- sourceBold %>% 
  set_names(c("x", "y", "z", "pitch", "roll", "yaw")) %>% 
  add_column(volume = 1:nrow(sourceBold), sequence = "bold") %>% 
  relocate("sequence", "volume","x", "y", "z", "pitch", "roll", "yaw")  %>% 
  pivot_longer(cols = c("x", "y", "z", "pitch", "roll", "yaw"),
               names_to = "motion_series", 
               values_to = "motion_param")

motion_regressor <-  bind_rows(vaso, bold)

# Translation

plot_xyz <- ggplot(data = subset(motion_regressor, motion_series == c("x", "y", "z")), 
                   aes(x = volume, 
                       y = motion_param,
                       colour = motion_series,
                       linetype = sequence)) +
  geom_hline(yintercept=0, 
             linetype="dashed",
             color = "lightgrey") +
  geom_hline(yintercept=.75,
             color = "red") +
  geom_hline(yintercept=-.75,
             color = "red") +
  geom_line() +
  theme_classic() +
  scale_y_continuous(limits = c(min(subset(vaso, motion_series == c("x", "y", "z"))[, "motion_param"]) - .05,
                                max(subset(vaso, motion_series == c("x", "y", "z"))[, "motion_param"]) + .05),
                     breaks = c(round(seq(from = min(subset(vaso, motion_series == c("x", "y", "z"))[, "motion_param"]) - .05, 
                                          to = max(subset(vaso, motion_series == c("x", "y", "z"))[, "motion_param"]) + .05, 
                                          by = 0.25), digits = 2))) +
  scale_x_continuous( limits = c(1, (nrow(motion_regressor)/(2*6)) + 2),
                      breaks = c(seq(from = 0, 
                                     to = (nrow(motion_regressor)/(2*6)) + 2, 
                                     by = 25))) 

# Rotation

plot_pry <- ggplot(data = subset(motion_regressor, motion_series == c("pitch", "roll", "yaw")), 
                   aes(x = volume, 
                       y = motion_param,
                       colour = motion_series,
                       linetype = sequence)) +
  geom_hline(yintercept=0, 
             linetype="dashed",
             color = "lightgrey") +
  geom_line() +
  theme_classic() +
  scale_y_continuous(limits = c(min(subset(vaso, motion_series == c("pitch", "roll", "yaw"))[, "motion_param"]) - .001,
                                max(subset(vaso, motion_series == c("pitch", "roll", "yaw"))[, "motion_param"]) + .001),
                     breaks = c(round(seq(from = min(subset(vaso, motion_series == c("pitch", "roll", "yaw"))[, "motion_param"]) - .01, 
                                          to = max(subset(vaso, motion_series == c("pitch", "roll", "yaw"))[, "motion_param"]) + .01, 
                                          by = 0.005), digits = 2))) +
  scale_x_continuous( limits = c(1, (nrow(motion_regressor)/(2*6)) + 2),
                      breaks = c(seq(from = 0, 
                                     to = (nrow(motion_regressor)/(2*6)) + 2, 
                                     by = 25))) 

plot_list <- list()

# plot 1
plot_list[[1]] <- plot_xyz

# plot 2
plot_list[[2]] <- plot_pry

# put them together
plot_2_save <- do.call(grid.arrange, c(plot_list, nrow=2))

# save it
ggsave(outputName,
       plot_2_save,    
       device="png",  
       path=mocoPath,
       units="cm",     
       width=15, 
       height=10, 
       dpi=300)

}
