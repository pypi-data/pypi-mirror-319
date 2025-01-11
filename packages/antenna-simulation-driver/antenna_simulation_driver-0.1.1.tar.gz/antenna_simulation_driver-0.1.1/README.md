# Antenna simulation driver and optimizer

## What?

This is a way of running the NEC2 antenna simulation
[nec2++](https://github.com/tmolteno/necpp).  You need to install that
yourself. See to it that the [pull request
82](https://github.com/tmolteno/necpp/pull/82) is on board,
otherwiese, this won't work. Finally, see to it that the `nec2++`
executable can be called, that is, is reachable via `PATH`.

## What not?

There is a [Python binding](https://pypi.org/project/PyNEC/) for
`nec2++`. I tried to get that to work, but failed. If that stuff
works for you, you probably don't need this.

So this is a pedestrian approach: Run `nec2++` in a separate
process and communicate with that process via stdin/stdout.

## Why?

- *Parameter studies.* Which terrible things happen if you make your
  antenna shorter and shorter, or lower and lower, or whatever.
- *Optimization.* Put this project and an appropriate
  [scipy optimization algorithm](https://docs.scipy.org/doc/scipy/reference/optimize.html#global-optimization)
  into a tumbler and stir well. Voila: A best antenna!

## How?

The `nec2pp_driver` is your entry point.  You need to feed it with a string
that contains the content you would usually put into a `.nec` file.

The problem: That format is neither documented here nor in the context
of the `nec2pp` project.  The NEC software traces its origin to the
1970s, when punched (paper) cards were commonplace. The original
input format for NEC2 software was defined in terms of such puched
cards. Old printed documentation of the day has been OCR'ed,
manually polished, and is now available at [www.nec2.org](https://www.nec2.org/).
In particular, the [NEC-2 manual](https://www.nec2.org/other/nec2prt3.pdf)
(converted from paper September 1996) is a good reference.

Today's nec2 implementations still read that stuff, even though they
are no longer as picky about column numbers as the old code used to be.

If you got your cards that you want to put into the simulation
as a Python string, and used an `RP` card to actually start
the simulation process somewhere in there, then my method
`run_nec2pp` of package `antenna_simulation_driver`
will run the simulation for you and give you a `Nec2ppOutput`
object back (defined in package `nec2pp_output_parser`)
that is a big bucket containing information about
the simulation run's result.

There is a showcase of how to actually use this stuff to do parameter
studies. It also has a few examples of useful card input to get
you started. This showcase is publicized via my personal block at
[https://dj3ei.famsik.de/blog/antennas/antenna_simulation_driver_showcase](https://dj3ei.famsik.de/blog/antennas/antenna_simulation_driver_showcase).

## Limitations

- The output parser has just started to catch information
  about the antenna's gain diagram and radiation diagram. 
  This is preliminary, largely untested, and may change
  depending on whether I like it or don't.

- One frequency, one call to `nec2pp_driver`.
  Don't yet specify more than one frequency in your `FR` card.
