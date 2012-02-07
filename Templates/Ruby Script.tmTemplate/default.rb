#!/usr/bin/env ruby
# encoding: utf-8
#
# Created by ${TM_FULLNAME} on ${TM_DATE}.
# Copyright (c) ${TM_YEAR} ${TM_ORGANIZATION_NAME}. All rights reserved.
#
require 'date'
require 'optparse'

if $0 == __FILE__
  options = {}
  OptionParser.new do |opts|
    opts.banner = "Usage: #{__FILE__} [OPTIONS]"
    opts.separator  ""
    opts.separator  "Example:"
    opts.separator  ""
    opts.separator  "OPTIONS"
    opts.on("-v", "--[no-]verbose", "Run verbosely") do |v|
      options[:verbose] = v
    end
  end.parse!

  puts ARGV
end