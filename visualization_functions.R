library(scales)
library(gt)
library(dplyr)
library(tidyr)
library(ggplot2)
library(ggpubr)
library(ggthemes)
library(glue)
library(ggrepel)
library(ggtext)
library(showtext)
library(ggforce)
library(readr)

category_scores <- data.frame(
  project_name = character(),
  category_name = character(),
  category_impact_number = integer(),
  category_index = double(),
  category_score = integer()
)

iu_palette <<- c(
  "#990000",
  "#FFAA00",
  "#006298",
  "#7D4C73",
  "#056E41"
)

spiral_palette <<- c(
  "1" = "#990000",
  "2" = "#F23A3F",
  "3" = "#FFD6DB",
  "4" = "#FFF7F8"
)

category_levels <<- c(
  "Participation",
  "Engagement",
  "Infrastructure",
  "Outputs",
  "Sustainability"
)

raw_impacts <<- c(
  "Participants",
  "Hours",
  "Infrastructures",
  "Outputs",
  "Partners"
)

credit_frame <- data.frame(
  x = 1,
  y = 1,
  label = glue("Community Engaged Research Balanced Expressions and Assessments with Nuanced Scores -- Generated {Sys.Date()} -- CC BY-NC-SA 4.0")
)
credit_line <<- ggplot(
  credit_frame,
  aes(
    x = x,
    y = y,
    label = label
  )
) +
  geom_richtext(
    fill = NA,
    label.color = NA,
    color = "#191919",
    size = 2.5
  ) +
  theme_light() +
  theme(
    legend.position = "none",
    axis.title = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.border = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "transparent"),
    plot.background = element_rect(fill = "transparent", color = NA)
  )

# Source and inspiration: https://datasketch.dev/post/2020-08-09-how-to-make-spirals-with-r/

bake_donut <- function(category_scores, the_project, the_overall) {
  the_frame <- category_scores |>
    filter(project_name == the_project)
  donut_labels <- vector()
  for (i in 1:5) {
    donut_labels[i] <- glue(
      "{the_frame$category_name[i]}\n{the_frame$category_index[i]}"
    )
  }
  donut_frame <- data.frame(
    names = category_levels,
    label = donut_labels,
    score = the_frame$category_index
  )
  donut_frame$names <- factor(
    donut_frame$names,
    levels = category_levels
  )
  bean_donut <- ggdonutchart(
    donut_frame, "score",
    fill = "names", color = "#EDEBEB",
    palette = iu_palette,
    lab.font = "#191919",
    # font.family = "rubik"
  ) +
    annotate(
      geom = "text",
      x = 0.5,
      y = 0,
      label = the_overall,
      size = 18,
      # family = "jetbrains"
    ) +
    theme(
      legend.position = "none",
      panel.background = element_rect(fill = "transparent"),
      plot.background = element_rect(fill = "transparent", color = NA),
      axis.ticks = element_blank()
    )
  return(bean_donut)
}

prep_raw <- function(category_scores, the_project) {
  the.frame <- category_scores |>
    filter(project_name == the_project)
  raw_labels <- vector()

  for (i in 1:5) {
    raw_labels[i] <- glue(
      "{category_scores$category_impact_number[i]} {raw_impacts[i]}"
    )
  }

  raw_frame <- data.frame(
    names = category_levels,
    label = raw_labels,
    values = the.frame$category_impact_number,
    bean = c("BEAN", "BEAN", "BEAN", "BEAN", "BEAN")
  )

  raw_frame$names <- factor(
    raw_frame$names,
    levels = rev(category_levels)
  )

  raw_frame$values_adjusted <- rescale(raw_frame$values, to = c(3, 100))

  raw_bar <- ggplot(raw_frame, aes(x = bean, y = values_adjusted, fill = names)) +
    geom_bar(
      stat = "identity",
      width = 1,
      color = "#EDEBEB"
    ) +
    coord_flip() +
    scale_fill_manual(values = rev(iu_palette)) +
    theme_light() +
    theme(
      legend.position = "none",
      axis.title = element_blank(),
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.border = element_blank(),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "transparent"),
      plot.background = element_rect(fill = "transparent", color = NA)
    )
  return(raw_bar)
}

prep_labels <- function(category_scores, the_project) {
  the_frame <- category_scores |>
    filter(project_name == the_project)
  label_frame <- data.frame(
    x = 1,
    y = 2,
    label = glue(
      "<span style='color:#99000088;'>█</span> <span style='color:#990000;'><b>{the_frame$category_impact_number[1]}</b></span> Participants <span style='color:#FFAA0088;'>█</span> <span style='color:#FFAA00;'><b>{the_frame$category_impact_number[2]}</b></span> Engagement Hours <span style='color:#00629888;'>█</span> <span style='color:#006298;'><b>{the_frame$category_impact_number[3]}</b></span> Infrastructure Products <span style='color:#59264D88;'>█</span> <span style='color:#59264D;'><b>{the_frame$category_impact_number[4]}</b></span> Outputs <span style='color:#056E4188;'>█</span> <span style='color:#056E41;'><b>{the_frame$category_impact_number[5]}</b></span> Partners"
    )
  )

  label_line <- ggplot(
    label_frame,
    aes(
      x = x,
      y = y,
      label = label
    )
  ) +
    geom_richtext(
      fill = NA,
      label.color = NA,
      color = "#191919",
      size = 3.5
    ) +
    theme_light() +
    theme(
      legend.position = "none",
      axis.title = element_blank(),
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.border = element_blank(),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "transparent"),
      plot.background = element_rect(fill = "transparent", color = NA)
    )
  return(label_line)
}

compile_badge <- function(the_donut, the_raw, the_labels, project_abbrev) {
  the_file <- glue("outputs/{project_abbrev}_badge.png")
  detailed_badge <- ggarrange(
    the_donut,
    the_raw,
    the_labels,
    credit_line,
    ncol = 1,
    nrow = 4,
    heights = c(8, 1, 1, 1)
  )
  ggsave(
    detailed_badge,
    filename = the_file,
    dpi = 320,
    width = 8,
    height = 8,
    units = "in"
  )
}

map_ripples <- function(the_project, the_frame) {
  the_project <- "PD @ TG"
  the_frame <- pdtg_ripple

  the_frame <- the_frame |>
    filter(project_name == the_project) |>
    select(-project_name)
  library(DiagrammeR)
  the_graph <- the_frame |>
    graph_from_data_frame(directed = TRUE)
}

map_spiral <- function(the_frame, the_colors, the_levels, the_grid) {
  the_frame <- the_frame |>
    mutate(values = ((values / sum(values)) * 100))
  the_frame$values <- round(the_frame$values, digits = 0)
  rep_frame <- rep(the_frame$name, times = the_frame$values)
  spiral_frame <- data.frame(
    group = rep_frame,
    x = vogel_coords$vogel_x,
    y = vogel_coords$vogel_y
  )
  the_spiral <- ggplot(spiral_frame) +
    geom_segment(
      aes(
        x = -10,
        y = 0,
        xend = 10,
        yend = 0
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = -10,
        xend = 0,
        yend = 10
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 8,
        yend = -8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 8,
        yend = 8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -8,
        yend = -8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -8,
        yend = 8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 1
      ),
      color = "#eeeeee",
      fill = "#ffffff"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 5
      ),
      color = "#eeeeee"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 10
      ),
      color = "#eeeeeecc"
    ) +
    geom_point(
      aes(
        x = 0,
        y = 0
      ),
      color = "#eeeeee",
      size = 2
    ) +
    geom_point(
      aes(
        x,
        y,
        color = group
      ),
      size = 6
    ) +
    coord_equal() +
    scale_color_manual(
      values = the_colors
    ) +
    theme_minimal() +
    theme(
      axis.ticks = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank(),
      panel.grid = element_blank(),
      legend.title = element_blank(),
      legend.position = "bottom",
      panel.background = element_rect(
        fill = "transparent",
        color = NA
      ),
      plot.background = element_rect(
        fill = "transparent",
        color = NA
      )
    )
}

vogel_spiral <- function(n) {
  t <- 1:n
  r <- sqrt(t)
  golden_angle <- pi * (3 - sqrt(5))
  theta <- t * golden_angle
  x <- r * cos(theta)
  y <- r * sin(theta)
  d <- tibble::tibble(x, y)
  d$n <- 1:n
  d
}

archimedean_spiral <- function(n, a = 0, b = 1, turns = 3) {
  # b separation of turns
  t <- seq(0, turns * 2 * pi, length.out = n)
  x <- (a + b * t) * cos(t)
  y <- (a + b * t) * sin(t)
  d <- tibble::tibble(x, y)
  d$n <- 1:n
  d
}

calculate_ripple <- function(the_frame) {
  the_frame$ripple_score <- lambda_ripple *
    (the_frame$values /
      (log(the_frame$group + 1)))
  the_frame <- the_frame |>
    mutate(
      ripple_score = if_else(
        is.infinite(ripple_score),
        values,
        ripple_score
      )
    )
  the_frame$ripple_score <- round(
    the_frame$ripple_score,
    digits = 0
  )
  the_frame$adj_score <- ((the_frame$ripple_score /
    sum(the_frame$ripple_score)) *
    100)
  the_frame$adj_score <- round(
    the_frame$adj_score,
    digits = 0
  )
  the_frame <- the_frame |>
    mutate(
      group_name = glue(
        "{values} {group_name}\n(η = {ripple_score})"
      )
    ) |>
    mutate(group = group + 1)
}

prepare_vogel <- function(the_frame) {
  rep_frame <- data.frame(
    group = rep(
      the_frame$group,
      times = the_frame$adj_score
    ),
    group_name = rep(
      the_frame$group_name,
      the_frame$adj_score
    )
  )
  spiral_frame <- vogel_spiral(sum(the_frame$adj_score))
  spiral_frame$group_name <- rep_frame$group_name
  spiral_frame$group <- rep_frame$group
  return(spiral_frame)
}

plot_vogel <- function(the_frame, the_labels) {
  the_frame$group <- factor(
    the_frame$group,
    levels = c(1:max(the_frame$group))
  )
  vogel_plot <- ggplot(the_frame) +
    geom_segment(
      aes(
        x = -10,
        y = 0,
        xend = 10,
        yend = 0
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = -10,
        xend = 0,
        yend = 10
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 8,
        yend = -8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 8,
        yend = 8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -8,
        yend = -8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -8,
        yend = 8
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 1
      ),
      color = "#eeeeee",
      fill = "#ffffff"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 5
      ),
      color = "#eeeeee"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 10
      ),
      color = "#eeeeee"
    ) +
    geom_point(
      aes(
        x = 0,
        y = 0
      ),
      color = "#eeeeee",
      size = 2
    ) +
    geom_point(
      aes(
        x,
        y,
        color = group
      ),
      size = 6
    ) +
    coord_equal() +
    scale_color_manual(
      labels = the_labels,
      values = spiral_palette
    ) +
    theme_minimal() +
    theme(
      axis.ticks = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank(),
      panel.grid = element_blank(),
      legend.title = element_blank(),
      legend.position = "bottom",
      panel.background = element_rect(
        fill = "transparent",
        color = NA
      ),
      plot.background = element_rect(
        fill = "transparent",
        color = NA
      )
    )
}

prep_composite <- function(the_frame, the_project) {
  composite_frame <- the_frame |>
    filter(project_name == the_project) |>
    mutate(category_name = glue("{category_name}\n(i = {category_index}, s = {category_score})")) |>
    mutate(category_score = category_score + 1)
  composite_frame$category <- c(1, 2, 3, 4, 5)
  composite_frame <- composite_frame |>
    mutate(adj_score = ((category_score / sum(category_score)) * 100))
  composite_frame$adj_score <- round(composite_frame$adj_score, digits = 0)
  return(composite_frame)
}

prep_arch <- function(the_frame) {
  arch_frame <- archimedean_spiral(sum(the_frame$adj_score))
  arch_frame$category_name <- rep(
    the_frame$category_name,
    times = the_frame$adj_score
  )
  arch_frame$category <- rep(
    the_frame$category,
    times = the_frame$adj_score
  )
  return(arch_frame)
}

plot_arch <- function(arch_frame, the_frame) {
  arch_frame$category <- factor(
    arch_frame$category,
    levels = c("1", "2", "3", "4", "5")
  )
  the_arch <- ggplot(arch_frame) +
    geom_segment(
      aes(
        x = -16,
        y = 0,
        xend = 16,
        yend = 0
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = -16,
        xend = 0,
        yend = 16
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 15,
        yend = -15
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = 15,
        yend = 15
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -15,
        yend = -15
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_segment(
      aes(
        x = 0,
        y = 0,
        xend = -15,
        yend = 15
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.01
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 1
      ),
      color = "#eeeeee",
      fill = "#ffffff"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 5
      ),
      color = "#eeeeee"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 10
      ),
      color = "#eeeeeecc"
    ) +
    geom_circle(
      aes(
        x0 = 0,
        y0 = 0,
        r = 15
      ),
      color = "#eeeeeecc"
    ) +
    geom_point(aes(x, y, color = category), size = 8) +
    coord_equal() +
    scale_color_manual(
      values = iu_palette,
      labels = the_frame$category_name
    ) +
    theme_minimal() +
    theme(
      legend.position = "bottom",
      axis.ticks = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank(),
      panel.grid = element_blank(),
      legend.title = element_blank(),
      panel.background = element_rect(
        fill = "transparent",
        color = NA
      ),
      plot.background = element_rect(
        fill = "transparent",
        color = NA
      )
    ) +
    guides(color = guide_legend(nrow = 1, byrow = TRUE))
  return(the_arch)
}

create_title_line <- function(title_description, title_score) {
  the_title <- data.frame(
    x = 1,
    y = 1,
    label = glue("{title_description} <b>{title_score}</b>")
  )
  title_line <<- ggplot(
    the_title,
    aes(
      x = x,
      y = y,
      label = label
    )
  ) +
    geom_richtext(
      fill = NA,
      label.color = NA,
      color = "#EDEBEB",
      size = 9
    ) +
    theme_light() +
    theme(
      legend.position = "none",
      axis.title = element_blank(),
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      panel.border = element_blank(),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      panel.background = element_rect(fill = "transparent"),
      plot.background = element_rect(fill = "#990000aa", color = "#990000aa")
    )
  return(title_line)
}

construct_bottom_badge <- function(arch_title, ripple_title, composite_arch, vogel_ripple) {
  bottom_badge <- ggarrange(
    arch_title,
    NULL,
    ripple_title,
    composite_arch,
    NULL,
    vogel_ripple,
    ncol = 3,
    nrow = 2,
    widths = c(14.5, 2, 14.5),
    heights = c(2, 14.5)
  )
  return(bottom_badge)
}

plot_indicators <- function(indicator_frame) {
  if (0 %in% indicator_frame$category_impact_number) {
    min_scale <- 0.01
  } else {
    min_scale <- ((min(indicator_frame$category_impact_number) /
      sum(indicator_frame$category_impact_number)) * 60) + 5
  }
  indicator_bubbles <- ggplot(indicator_frame) +
    geom_segment(
      aes(
        x = 0,
        y = 1,
        xend = 6,
        yend = 1
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_segment(
      aes(
        x = 1,
        y = -0.75,
        xend = 1,
        yend = 2.75
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_segment(
      aes(
        x = 3,
        y = -0.75,
        xend = 3,
        yend = 2.75
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_segment(
      aes(
        x = 2,
        y = -0.75,
        xend = 2,
        yend = 2.75
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_segment(
      aes(
        x = 4,
        y = -0.75,
        xend = 4,
        yend = 2.75
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_segment(
      aes(
        x = 5,
        y = -0.75,
        xend = 5,
        yend = 2.75
      ),
      color = "#eeeeee",
      linetype = "solid",
      linewidth = 0.5
    ) +
    geom_point(
      aes(
        x = 1,
        y = 1
      ),
      shape = 21, color = "#eeeeee", fill = "transparent", size = 60, stroke = 0.5
    ) +
    geom_point(
      aes(
        x = 2,
        y = 1
      ),
      shape = 21, color = "#eeeeee", fill = "transparent", size = 60, stroke = 0.5
    ) +
    geom_point(
      aes(
        x = 3,
        y = 1
      ),
      shape = 21, color = "#eeeeee", fill = "transparent", size = 60, stroke = 0.5
    ) +
    geom_point(
      aes(
        x = 4,
        y = 1
      ),
      shape = 21, color = "#eeeeee", fill = "transparent", size = 60, stroke = 0.5
    ) +
    geom_point(
      aes(
        x = 5,
        y = 1
      ),
      shape = 21, color = "#eeeeee", fill = "transparent", size = 60, stroke = 0.5
    ) +
    geom_point(aes(
      x = x,
      y = y,
      size = category_impact_number,
      color = category_name
    )) +
    xlim(0, 6) +
    ylim(-0.75, 2.75) +
    scale_color_manual(
      values = iu_palette,
      labels = indicator_frame$category_labels
    ) +
    scale_size(range = c(min_scale, 60)) +
    guides(
      fill = FALSE,
      size = FALSE
    ) +
    theme_minimal() +
    theme(
      legend.position = "bottom",
      axis.ticks = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank(),
      panel.grid = element_blank(),
      legend.title = element_blank(),
      panel.background = element_rect(
        fill = "transparent",
        color = NA
      ),
      plot.background = element_rect(
        fill = "transparent",
        color = NA
      )
    )
  return(indicator_bubbles)
}

construct_badge <- function(indicator_title, indicator_plot, bottom_badge) {
  full_badge <- ggarrange(
    indicator_title,
    indicator_plot,
    bottom_badge,
    credit_line,
    ncol = 1,
    nrow = 4,
    heights = c(
      1.5,
      8,
      16,
      1
    )
  )
}

deh_ripple <- deh_ripple |> calculate_ripple()

deh_vogel_frame <- deh_ripple |> prepare_vogel()

deh_vogel_ripple <- deh_vogel_frame |> plot_vogel(deh_ripple$group_name)

deh_composite_ripple_score <- sum(deh_ripple$ripple_score)

deh_overall_score <- calculate_overall(category_scores, "DEH")

category_names <- c(
  "Sustainability",
  "Outputs",
  "Infrastructure",
  "Engagement",
  "Participation"
)

deh_composite_frame <- category_scores |>
  prep_composite("DEH")

deh_arch_frame <- deh_composite_frame |>
  prep_arch()

deh_composite_arch <- deh_arch_frame |>
  plot_arch(deh_composite_frame)

deh_arch_title <- create_title_line("Composite Impact Score", deh_overall_score)

deh_ripple_title <- create_title_line("Ripple Effect Score", deh_composite_ripple_score)

indicator_weights <- data.frame(
  weights = c(
    participants_weight,
    engagement_weight,
    infrastructure_weight,
    outputs_weight,
    sustainability_weight
  )
)

deh_composite_indicator_score <- calculate_indicator_score(
  category_scores,
  "DEH",
  indicator_weights
)

deh_indicator_title <- create_title_line("Direct Indicator Score", deh_composite_indicator_score)

deh_bottom_badge <- construct_bottom_badge(
  deh_arch_title,
  deh_ripple_title,
  deh_composite_arch,
  deh_vogel_ripple
)

deh_indicator_frame <- prep_indicators(category_scores, "DEH")

deh_indicator_plot <- plot_indicators(deh_indicator_frame)

deh_badge <- construct_badge(
  deh_indicator_title,
  deh_indicator_plot,
  deh_bottom_badge
)
ggsave("outputs/deh_dashboard.png", deh_badge, width = 16, height = 10, units = "in", dpi = 320)