#!/usr/bin/env ruby
# encoding: utf-8
#
# Created by ${TM_FULLNAME} on ${TM_DATE}.
# Copyright (c) ${TM_YEAR} ${TM_ORGANIZATION_NAME}. All rights reserved.
#
require 'date'
require 'optparse'
require 'awesome_print'

if $0 == __FILE__
  options = {}
  opt_parser = OptionParser.new do |opt|
    opt.banner = "Usage: #{__FILE__} [OPTIONS] [ARGUMENTS]"
    opt.separator  ""
    opt.separator  "OPTIONS"
    opt.on("-s", "--server SERVER", "Hostname") do |hostname|
      options[:hostname] = hostname
    end
    opt.on("-v", "--[no-]verbose", "Run verbosely") do |v|
      options[:verbose] = v
    end
    opt.separator  ""
    opt.separator  "ARGUMENTS"
    opt.separator  ""
  end
  opt_parser.parse!
  
  ap options
end
