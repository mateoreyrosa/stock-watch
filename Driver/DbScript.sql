USE [master]
GO
/****** Object:  Database [StockData]    Script Date: 5/7/2020 9:55:26 PM ******/
CREATE DATABASE [StockData]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'StockData', FILENAME = N'/var/opt/mssql/data/StockData.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 10%)
 LOG ON
( NAME = N'StockData_log', FILENAME = N'/var/opt/mssql/data/StockData_log.ldf' , SIZE = 1024KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [StockData] SET COMPATIBILITY_LEVEL = 140
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [StockData].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
USE [StockData]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Process](
	[SymbolsProcessed] [bit] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Symbol]    Script Date: 5/7/2020 9:55:27 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Symbol](
	[Symbol] [varchar](100) NOT NULL,
	[Name] [varchar](1000) NULL,
	[MarketOpenPrice] [decimal](12, 4) NULL,
	[IsProcessingPrice] [bit] NULL,
 CONSTRAINT [PK_Symbol] PRIMARY KEY CLUSTERED
(
	[Symbol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [StockData] SET  READ_WRITE
GO
