# Next Day Video

The fantastic @CarlFK from NextDayVideo.com will work with us on occasion for
video production.  In order to work with him we need to expose a few pieces of
information to enable the Veyepar workflow.

# Workflow

## Data Requirements

This page documents what is needed. https://github.com/CarlFK/veyepar/wiki/Asking-for-Videos
Below are the fields needed and how they map to our internal objects and settings.

    Title - Topic.title
    Description - Topic.description
    Name presenter(s) - Presenter.name (list)
    Presenter Email - Presenter.email (list)
    Reviewer (email) - TALK_REVIEWERS environmental variable (list)
    Date of talk - Meeting.when
    Time of talk (estimate) - Meeting.when
    Duration of talk (estimate) - Topic.length

Key points:

* Reviewers should never be more than 3, by preference of @CarlFK

## Data Retrieval

The pull comes from https://www.chipy.org/api/meetings/
